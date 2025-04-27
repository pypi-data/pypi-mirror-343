import os
import numpy as np
import argparse
import math
import pandas as pd
from pyne import mcnp
from pyne.mesh import MeshTally, HAVE_PYMOAB
import matplotlib.pyplot as plt
import seaborn as sns
from configparser import ConfigParser
from natf.utils import format_single_output
import configparser
import re


def get_ptype(particle='neutron'):
    ptype = 'n'
    if particle.lower() in ['n', 'neutron']:
        ptype = 'n'
    elif particle.lower() in ['p', 'photon']:
        ptype = 'p'
    return ptype


def create_tag_content(particle='neutron'):
    """
    Create tags according to the tally_nums and particle.

    Parameters:
    -----------
    particle: string
        particle type, allowed particle: 'neutron', 'n', 'photon', 'p'
    """
    ptype = get_ptype(particle)
    tag_content = [f'{ptype}_result', f'{ptype}_rel_error',
                   f'{ptype}_total_result', f'{ptype}_total_rel_error']
    return tag_content


def create_tags(tally_nums, particle='n'):
    if isinstance(tally_nums, int):
        tally_nums = [tally_nums]
    tags = {}
    tag_content = create_tag_content(particle=particle)
    for tid in tally_nums:
        tags[tid] = tag_content
    return tags


def meshtally2h5m(meshtally):
    """
    Convert meshtally data to h5m.

    Parameters:
    -----------
    meshtally: pyne.mesh MeshTally object
        The meshtally to be converted.
    ofname: str
        output file name
    """

    tally_num = meshtally.tally_number
    ofname = f"meshtally{tally_num}.h5m"
    meshtally.write_hdf5(ofname, write_mats=False)
    return


def meshtally_evaluation(meshtally, ctm=None, tag_name='n_total_rel_error'):
    """
    Some typical analyses value are evaluated.
    - score percentage, eta: ratio of non_zero mesh elements / total mesh elements
    - effective score percentage:
        - eta_eff_10: ratio of mesh elements with rel_err < 0.1 / non_zero mesh elements
        - eta_eff_5: ratio of mesh elements with rel_err < 0.05 / non_zero mesh elements
    - Global Figure-of-Merit, FOG_g: fom_g = 1/(ctm * SIG(rel_err**2) / num_ves)
        - Note: for those elements with zero rel_err (not tallied), rel_err should be
                replaced with 1.0

    Parameters:
    -----------
    meshtally: PyNE MeshTally object
        meshtally to analysis
    ctm: float
        Compute time in minutes
    tag_name: str
        Total relative error tag name.

    Returns:
    --------
    eta, eta_eff_10, eta_eff_5, fom_g, sig_re
    """

    num_ves = meshtally.num_ves
    # calculate eta and eta_eff_10, eta_eff_5
    num_nonzero = 0
    num_eff_10 = 0
    num_eff_5 = 0
    total_rel_error = getattr(meshtally, tag_name)[:]
    for i, rel_err in enumerate(total_rel_error):
        if rel_err > 0:
            num_nonzero += 1
        if rel_err > 0 and rel_err < 0.1:
            num_eff_10 += 1
        if rel_err > 0 and rel_err < 0.05:
            num_eff_5 += 1
    eta = num_nonzero/float(num_ves)
    eta_eff_10 = num_eff_10/float(num_nonzero)
    eta_eff_5 = num_eff_5/float(num_nonzero)

    if ctm is None:
        print(f"ctm is not given, FOM_g will not be calculated")
        return eta, eta_eff_10, eta_eff_5, 0.0
    # reset 0.0 rel_err to 1
    sum_rel_err_squre = 0.0
    for i, rel_err in enumerate(total_rel_error):
        if rel_err == 0.0:
            total_rel_error[i] = 1.0
        sum_rel_err_squre += rel_err * rel_err
    # calculate fom_g
    # FOG_m = 1/(ctm * SIG(rel_err**2) / num_ves)
    fog_m = 1.0 / (ctm * sum_rel_err_squre / num_ves)

    return eta, eta_eff_10, eta_eff_5, fog_m


def remove_tally_fc(filename):
    """
    Remove the comment line of tally results.
    """
    tmpout = 'tmpout'
    fo = open(tmpout, 'w')
    with open(filename, 'r') as fin:
        tally_start = False
        while True:
            line = fin.readline()
            if line == '':
                break
            if 'Mesh Tally Number' in line:
                fo.write(line)
                line = fin.readline()
                if ('neutron' not in line) and ('photon' not in line):  # comment line
                    pass
                else:
                    fo.write(line)
            else:
                fo.write(line)
    # close w file
    fo.close()
    # remove the old file and name to new file
    os.remove(filename)
    os.system(f"mv {tmpout} {filename}")

    return


def get_tally_nums(filename):
    """
    Read meshtal file to get tally numbers.

    Parameters:
    -----------
    filename: str
        The filename of the meshtal.

    Returns:
    --------
    tally_nums: list
        List of tally numbers
    """
    tally_nums = []
    with open(filename, 'r') as fin:
        while True:
            line = fin.readline()
            if line == '':
                break
            if 'Mesh Tally Number' in line:
                tokens = line.strip().split()
                tid = int(tokens[-1])
                tally_nums.append(tid)
    return tally_nums


def plot_pdf_vs_rel_err(meshtally, tag_name='n_total_rel_error', ofname='pdf_err.png', bins=20):
    """
    Plot the probability distribution function vs. relative error.
    """
    # make the plot
    total_rel_error = getattr(meshtally, tag_name)
    sns.set_style('darkgrid')
    ax = sns.histplot(total_rel_error[:], bins=bins)
    # tidy up the figure
    # ax.legend(loc='best')
    ax.set_xlabel('Relative error')
    ax.set_ylabel('Frequency')
    fig = ax.get_figure()
    fig.savefig(ofname, dpi=600, bbox_inches='tight')
    plt.close()
    return


def plot_cdf_vs_rel_err(meshtally, tag_name='n_total_rel_error', ofname='cdf_err.png', bins=None):
    """
    Plot the cumulative probabitity distribution function vs. relative error.
    """
    total_rel_error = getattr(meshtally, tag_name)
    # set up bins
    if bins is None:
        num_ves = meshtally.num_ves
        if num_ves < 5:
            bins = num_ves
        elif num_ves < 20:
            bins = 5
        elif num_ves < 100:
            bins = 20
        elif num_ves < 1e4:
            bins = 50
        else:
            bins = 100
    values, base = np.histogram(total_rel_error[:], bins=bins)
    # evaluate the culmulative
    normed_values = values / sum(values)
    cumulative = np.cumsum(normed_values)
    sns.set_style("darkgrid")
    ax = sns.lineplot(x=base[:-1], y=cumulative)
    # ax.set(title='Cumulative probability distribution of relative error')
    ax.set(xlabel='Relative error')
    ax.set_ylabel('Cumulative density')
    # ax.legend(loc='best')
    fig = ax.get_figure()
    fig.savefig(ofname, dpi=600, bbox_inches='tight')
    plt.close()
    return


def get_ctm(filename):
    """
    Read log file to get ctm.
    """
    ctm = -1.0
    with open(filename, 'r') as fin:
        while True:
            line = fin.readline()
            if line == '':
                break
            if 'ctm =' in line:
                ctm = float(line.strip().split()[2])
    if ctm < 0:
        raise ValueError(f"ctm not found in {filename}")
    return ctm


def scale_with_multiplier(meshtally, multiplier, particle):
    """
    Multiply the result with multiplier
    """
    ptype = get_ptype(particle)
    # result
    result_tag_name = f"{ptype}_result"
    result = getattr(meshtally, result_tag_name)[:]
    result = np.multiply(result, multiplier)
    # total result
    total_result_tag_name = f"{ptype}_total_result"
    total_result = getattr(meshtally, total_result_tag_name)[:]
    total_result = np.multiply(total_result, multiplier)
    if ptype == 'n':
        meshtally.n_result[:] = result[:]
        meshtally.n_total_result[:] = total_result[:]
    elif ptype == 'p':
        meshtally.p_result[:] = result[:]
        meshtally.p_total_result[:] = total_result[:]
    return meshtally


def calc_midx(r, x_bounds, y_bounds, z_bounds):
    """
    Calculate the index of the mesh element.
    """
    # boundary check
    if r[0] < x_bounds[0] or r[0] > x_bounds[-1]:
        raise ValueError(f"point {r} out of x-dimension range")
    if r[1] < y_bounds[0] or r[1] > y_bounds[-1]:
        raise ValueError(f"point {r} out of y-dimension range")
    if r[2] < z_bounds[0] or r[2] > z_bounds[-1]:
        raise ValueError(f"point {r} out of z-dimension range")

    # calculate the index
    xidx = min(np.searchsorted(
        x_bounds, r[0], side='right'), len(x_bounds)-1) - 1
    yidx = min(np.searchsorted(
        y_bounds, r[1], side='right'), len(y_bounds)-1) - 1
    zidx = min(np.searchsorted(
        z_bounds, r[2], side='right'), len(z_bounds)-1) - 1
    midx = zidx + yidx*(len(z_bounds)-1) + xidx * \
        (len(y_bounds)-1)*(len(z_bounds)-1)
    if midx > (len(x_bounds)-1)*(len(y_bounds)-1)*(len(z_bounds)-1):
        raise ValueError(f"WARNING: point {r} out of mesh")
    return midx


def calc_midxes_in_box(box, x_bounds, y_bounds, z_bounds):
    """
    Calculate the indexes of the mesh element in the box.
    """
    # lower conner
    xidx_min = min(np.searchsorted(
        x_bounds, box[0], side='right'), len(x_bounds)-1) - 1
    xidx_max = np.searchsorted(x_bounds, box[3]) - 1
    yidx_min = min(np.searchsorted(
        y_bounds, box[1], side='right'), len(y_bounds)-1) - 1
    yidx_max = np.searchsorted(y_bounds, box[4]) - 1
    zidx_min = min(np.searchsorted(
        z_bounds, box[2], side='right'), len(z_bounds)-1) - 1
    zidx_max = np.searchsorted(z_bounds, box[5]) - 1
    indexes = []
    for i in range(xidx_min, xidx_max+1):
        for j in range(yidx_min, yidx_max+1):
            for k in range(zidx_min, zidx_max+1):
                midx = k + j*(len(z_bounds)-1) + i * \
                    (len(y_bounds)-1)*(len(z_bounds)-1)
                indexes.append(midx)
    return indexes


def calc_eidx(energy, e_bounds):
    """
    Calculate the energy index (eidx) for a given energy based on the energy bounds (e_bounds).

    Parameters:
    energy (float): The energy value to find the index for.
    e_bounds (list of float): The list of energy bounds.

    Returns:
    int: The index of the energy bin that the energy falls into.
    """
    if energy < e_bounds[0]:
        raise ValueError(
            f"Energy {energy} is out of the lower bound {e_bounds[0]}")
    if energy == e_bounds[0]:
        return 0
    for i in range(len(e_bounds) - 1):
        if e_bounds[i] < energy <= e_bounds[i + 1]:
            return i
    # If energy is equal to or greater than the last bound
    return len(e_bounds) - 1


def get_value_by_midxes(meshtally, midxes):
    values = []
    result_total_tag_name = f"n_total_result"
    results_total = getattr(meshtally, result_total_tag_name)[:]
    for idx in midxes:
        if idx < len(results_total):
            values.append(results_total[idx])
    return values


def get_result_by_pos(meshtally, r, particle='n', ofname='result.txt', style='fispact', verbose_string=None):
    """
    Get the result of specific position.
    """
    midx = calc_midx(r, meshtally.x_bounds,
                     meshtally.y_bounds, meshtally.z_bounds)
    ptype = get_ptype(particle)
    result_tag_name = f"{ptype}_result"
    results = getattr(meshtally, result_tag_name)[:]
    result = results[midx]
    result_total_tag_name = f"{ptype}_total_result"
    results_total = getattr(meshtally, result_total_tag_name)[:]
    result_total = results_total[midx]
    if isinstance(result, float):
        result = [result]
    with open(ofname, 'w') as fo:
        if style == 'fispact':
            for i in range(len(result)):  # reverse the neutron flux
                fo.write(
                    ''.join([format_single_output(result[len(result) - 1 - i]), '\n']))
            fo.write('1.0\n')
            fo.write(' '.join(['Neutron energy group', str(
                len(result)), 'G, TOT = ', format_single_output(result_total)]))
            if verbose_string:
                fo.write(f"\n# {verbose_string}")
        else:
            raise ValueError(f"style {style} not supported")
    fo.close()


def get_result_by_config(pos_config):
    conf = ConfigParser()
    conf.read(pos_config)
    file_info = conf.sections()

    # Read the necessary files once
    df = pd.read_csv(conf['general']['pos_file'])
    print(f"reading positions from {conf['general']['pos_file']}")
    mc_file = conf['general']['mc_file']
    print(f"reading meshtal from {mc_file}")
    output_file = conf['general']['output_file']
    print(f"results will be writen in {output_file}")
    read_whole_mesh = True
    try:
        read_whole_mesh = conf['general'].getboolean(
            'read_whole_mesh', fallback=True)
    except:
        pass
    print(f"read_whole_mesh: {read_whole_mesh}")

    # read the positons from the pos_file
    coordinates = df['Coordinate'].apply(
        lambda pos_str: list(map(float, pos_str.strip().split())))

    # Precompute bounds and lengths
    x_bounds = None
    y_bounds = None
    z_bounds = None

    for column in file_info[1:]:
        particle = conf[column]['particle']
        tally_id = conf[column].getint('tally_id')
        pos_name = conf[column]['id_name']
        ptype = get_ptype(particle)
        multiplier = conf[column].getfloat('multiplier')

        if read_whole_mesh:
            tags = create_tags(tally_id, particle=particle)
            print(
                f"    reading meshtally for tally {tally_id}, particle type: {particle}")
            meshtal = MeshtalWithNumber(
                mc_file, tags=tags, tally_number=tally_id)
            meshtally = meshtal.tally[tally_id]
            multiplier = conf[column].getfloat('multiplier')
            print(
                f"    scale the meshtally results with multiplier {multiplier}")
            meshtally = scale_with_multiplier(meshtally, multiplier, particle)

            if x_bounds is None:
                x_bounds = meshtally.x_bounds
                y_bounds = meshtally.y_bounds
                z_bounds = meshtally.z_bounds

            result_tag_name = f"{ptype}_result"
            error_tag_name = f"{ptype}_rel_error"
            result_total_tag_name = f"{ptype}_total_result"
            error_total_tag_name = f"{ptype}_total_rel_error"

            results = getattr(meshtally, result_tag_name)
            errors = getattr(meshtally, error_tag_name)
            results_total = getattr(meshtally, result_total_tag_name)
            errors_total = getattr(meshtally, error_total_tag_name)

            for i, pos in enumerate(coordinates):
                print(f"        dealing with {i}-th position: {pos}")
                midx = calc_midx(pos, x_bounds, y_bounds, z_bounds)
                result = results[midx]
                error = errors[midx]
                result_total = results_total[midx]
                error_total = errors_total[midx]

                for j in range(len(meshtally.e_bounds) - 1):
                    df.at[i, f"{pos_name}_e_{meshtally.e_bounds[j+1]}_result"] = result[j]
                    df.at[i, f"{pos_name}_e_{meshtally.e_bounds[j+1]}_error"] = error[j]
                df.at[i, f"{pos_name}_{result_total_tag_name}"] = result_total
                df.at[i, f"{pos_name}_{error_total_tag_name}"] = error_total
        else:  # read the data of specific positions
            print(f"    reading bounds for tally {tally_id}")
            x_bounds, y_bounds, z_bounds, e_bounds = read_mesh_bounds(
                mc_file, tally_id)
            if len(e_bounds) > 2:
                e_data_count = len(e_bounds)
            else:
                e_data_count = 1
            print(
                f"    reading meshtally for tally {tally_id}, particle type: {particle}")
            data = extract_data_from_tally(
                mc_file, tally_id, coordinates, multiplier=multiplier)
            for i, pos in enumerate(coordinates):
                print(f"        dealing with {i}-th position: {pos}")
                xidx = np.searchsorted(x_bounds, pos[0], side='right') - 1
                yidx = np.searchsorted(y_bounds, pos[1], side='right') - 1
                zidx = np.searchsorted(z_bounds, pos[2], side='right') - 1
                midx = zidx + yidx * (len(z_bounds) - 1) + xidx * \
                    (len(y_bounds) - 1) * (len(z_bounds) - 1)
                for j in range(len(e_bounds) - 1):
                    df.at[i, f"{pos_name}_e_{e_bounds[j+1]}_result"] = data[data['midx']
                                                                            == midx]['result'][j]
                    df.at[i, f"{pos_name}_e_{e_bounds[j+1]}_error"] = data[data['midx']
                                                                           == midx]['rel_error'][j]
                df.at[i, f"{pos_name}_{ptype}_total_result"] = data[data['midx']
                                                                    == midx]['result'][e_data_count-1]
                df.at[i, f"{pos_name}_{ptype}_total_rel_error"] = data[data['midx']
                                                                       == midx]['rel_error'][e_data_count-1]

    print(f"writing results in {output_file}")
    df.to_csv(output_file, sep=',', index=True)


def get_result_by_positions(meshtally, names, positions, locations, particle='n', style='fispact', verbose_string=None):
    """
    Get the result of specific position.
    """
    for i, pos in enumerate(positions):
        if names[i] != '':
            ofname = f'{names[i]}.txt'
        else:
            ofname = f'pos{i+1}.txt'
        midx = calc_midx(pos, meshtally.x_bounds,
                         meshtally.y_bounds, meshtally.z_bounds)
        ptype = get_ptype(particle)
        result_tag_name = f"{ptype}_result"
        results = getattr(meshtally, result_tag_name)[:]
        result = results[midx]
        result_total_tag_name = f"{ptype}_total_result"
        results_total = getattr(meshtally, result_total_tag_name)[:]
        result_total = results_total[midx]
        if isinstance(result, float):
            result = [result]
        with open(ofname, 'w') as fo:
            if style == 'fispact':
                for j in range(len(result)):  # reverse the neutron flux
                    fo.write(
                        ''.join([format_single_output(result[len(result) - 1 - j]), '\n']))
                fo.write('1.0\n')
                fo.write(f"# location: {locations[i]}\n")
                fo.write(f"# Position: {pos[0]} {pos[1]} {pos[2]}\n")
                fo.write(
                    f"# Neutron energy group: {len(result)}, TOT = {format_single_output(result_total)}\n")
                if verbose_string:
                    fo.write(f"# {verbose_string}")
            else:
                raise ValueError(f"style {style} not supported")
        fo.close()


def parse_positions(filename):
    """
    parse the positions defined in pos_file.

    Returns:
    --------
    positions : list of list
        The list of boxes (list with 3 float defining x, y, z)
    """
    positions = []
    names = []
    locations = []
    with open(filename, 'r') as fin:
        line = fin.readline()
        while True:
            line = fin.readline()
            if line == '':
                break
            name, coordinate, location = line.split(",")
            tokens = coordinate.split()
            if len(tokens) == 0:
                pass
            if len(tokens) != 3:
                raise ValueError(f"line {line} with wrong format")
            pos = [float(tokens[0]), float(tokens[1]), float(tokens[2])]
            location = location.strip("\n")
            names.append(name)
            positions.append(pos)
            locations.append(location)
    return names, positions, locations


def parse_boxes(filename):
    """
    parse the boxes defined in box_file.

    Returns:
    --------
    boxes : list of list
        The list of boxes (list with 6 float defining xmin, ymin, zmin, xmax, ymax, zmax)
    """
    boxes = []
    names = []
    with open(filename, 'r') as fin:
        count = 0
        while True:
            line = fin.readline()
            if line == '':
                break
            tokens = line.split()
            if len(tokens) == 6:
                count += 1
                box = [float(tokens[0]), float(tokens[1]), float(tokens[2]),
                       float(tokens[3]), float(tokens[4]), float(tokens[5])]
                name = f"box{count}"
            elif len(tokens) == 7:
                box = [float(tokens[0]), float(tokens[1]), float(tokens[2]),
                       float(tokens[3]), float(tokens[4]), float(tokens[5])]
                name = tokens[6]
            else:
                raise ValueError(f"line {line} with wrong format")
            boxes.append(box)
            names.append(name)
    return boxes, names


def rotate_point_to_angle_range(pos, angle_range=360):
    """
    Rotate a point to the defined angle range
    """
    # calculate the R on x-y plane
    r_squred = pos[0] * pos[0] + pos[1] * pos[1]
    r = math.sqrt(r_squred)
    angle = np.angle(pos[0]+pos[1]*(0+1j), deg=True)
    new_angle = (angle+360+angle_range) % angle_range - angle_range
    pos[0] = r*math.cos(new_angle/180*math.pi)
    pos[1] = r*math.sin(new_angle/180*math.pi)
    return pos


def rotate_box(box, angle_range=360):
    """
    rotate a box
    """
    lp = rotate_point_to_angle_range(box[0:3], angle_range)
    up = rotate_point_to_angle_range(box[3:], angle_range)
    return [lp[0], lp[1], lp[2], up[0], up[1], up[2]]


def get_value_by_corner_center(meshtally, box, angle_range=360):
    """
    get the values of corner and center of the box
    """
    x_bounds = meshtally.x_bounds
    y_bounds = meshtally.y_bounds
    z_bounds = meshtally.z_bounds
    # add corners and center
    points = []
    # corners
    points.append(box[0:3])
    points.append([box[0], box[1], box[5]])
    points.append([box[0], box[4], box[0]])
    points.append([box[0], box[4], box[5]])
    points.append([box[3], box[1], box[2]])
    points.append([box[3], box[1], box[5]])
    points.append([box[3], box[4], box[2]])
    points.append(box[3:])
    # surf-center
    points.append([(box[0]+box[3])/2, box[1], (box[2]+box[5])/2])
    points.append([(box[0]+box[3])/2, box[4], (box[2]+box[5])/2])
    points.append([(box[0]+box[3])/2, (box[1]+box[4])/2, box[2]])
    points.append([(box[0]+box[3])/2, (box[1]+box[4])/2, box[5]])
    points.append([box[0], (box[1]+box[4])/2, (box[2]+box[5])/2])
    points.append([box[3], (box[1]+box[4])/2, (box[2]+box[5])/2])
    # center
    points.append([(box[0]+box[3])/2, (box[1]+box[4])/2,
                  (box[2]+box[5])/2])

    # rotate points to angle range
    for i in range(len(points)):
        points[i] = rotate_point_to_angle_range(
            points[i], angle_range=angle_range)

    midxes = []
    for p in points:
        midxes.append(calc_midx(p, x_bounds, y_bounds, z_bounds))
    values = get_value_by_midxes(meshtally, midxes)
    return values

# check whether a line is header line of a tally


def is_tally_header(line):
    """
    Determines if a given line is a tally header.

    A tally header is identified by the first three words being "Mesh", "Tally", and "Number".

    Args:
        line (str): A line of text to be checked.

    Returns:
        bool: True if the line is a tally header, False otherwise.
    """
    if line.split()[0:3] == ["Mesh", "Tally", "Number"]:
        return True
    return False

# read mesh bounds from a meshtal file with specific tally number


def read_mesh_bounds(filename, tally_num):
    """
    Read the mesh bounds from a meshtal file for a specific tally number.

    Args:
        filename (str): The meshtal file to read from.
        tally_num (int): The tally number to read the mesh bounds for.

    Returns:
        tuple of numpy.ndarray: The x, y, z and e mesh bounds.
    """
    with open(filename, "r") as f:
        while True:
            line = f.readline()
            if line == "":
                break
            if is_tally_header(line):
                if int(line.split()[3]) == tally_num:
                    while True:
                        line = f.readline()
                        if line == "":
                            break
                        if "Tally bin boundaries:" in line:
                            x_bounds = np.array(
                                [float(x) for x in f.readline().split(':')[-1].split()])
                            y_bounds = np.array(
                                [float(x) for x in f.readline().split(':')[-1].split()])
                            z_bounds = np.array(
                                [float(x) for x in f.readline().split(':')[-1].split()])
                            e_bounds = np.array(
                                [float(x) for x in f.readline().split(':')[-1].split()])
                            return x_bounds, y_bounds, z_bounds, e_bounds
    raise LookupError(f"tally number {tally_num} not found in {filename}")


def is_tally_data_header(line):
    """
    Determines if a given line is a tally data header.

    A tally data header is identified by the first five words being "Energy", "X", "Y", "Z", and "Result".

    Args:
        line (str): A line of text to be checked.

    Returns:
        bool: True if the line is a tally data header, False otherwise.
    """
    if "X         Y         Z     Result     Rel Error" in line:
        return True
    return False


def has_energy_bin_in_tally_result(line):
    """
    Determines if a given line has energy bin.

    Args:
        line (str): A line of text to be checked.

    Returns:
        bool: True if the line has energy bin, False otherwise.
    """
    if is_tally_data_header(line):
        if "Energy" in line:
            return True
    else:
        return False
    return False

# extract specific data from a tally with given positions


def extract_data_from_tally(filename, tally_num, positions, multiplier=1.0):
    """
    Extracts data from a tally for specific positions.

    Args:
        filename: The meshtal to extract data from.
        positions (list of list of float): The positions to extract data for.
        particle (str): The type of particle to extract data for.
        multiplier (float): The multiplier to apply to the data.

    Returns:
        list of dict: A list of dictionaries containing the data for each position.
    """
    x_bounds, y_bounds, z_bounds, e_bounds = read_mesh_bounds(
        filename, tally_num)
    # let data to be a numpy array with columns: energy, x, y, z, result, error, midx
    if len(e_bounds) > 2:
        e_data_count = len(e_bounds)
    else:
        e_data_count = 1
        print(
            "        WARNING: no detail energy bins in the meshtally {tally_num}, only total bin")
    data = np.zeros(len(positions)*e_data_count, dtype=[(str('midx'), np.int64),
                                                        (str('eidx'), np.int64),
                                                        (str('result'),
                                                         np.float64),
                                                        (str('rel_error'), np.float64)])
    midxes_request = []
    print(f"        calculating midx for positions")
    for pos in positions:
        midx = calc_midx(pos, x_bounds, y_bounds, z_bounds)
        midxes_request.append(midx)
    with open(filename, "r") as f:
        while True:
            line = f.readline()
            if line == "":
                break
            if is_tally_header(line):
                if int(line.split()[3]) == tally_num:
                    while True:
                        line = f.readline()
                        if line == "":
                            break
                        if is_tally_data_header(line):
                            print(
                                f"            reading tally data for tally {tally_num}")
                            if has_energy_bin_in_tally_result(line):
                                items_count = 6
                                shift = 1
                            else:
                                items_count = 5
                                shift = 0
                            # read the data
                            count = 0
                            while True:
                                line = f.readline()
                                if line == "" or line == "\n":
                                    break
                                tokens = line.split()
                                if len(tokens) == items_count:
                                    if items_count == 6:
                                        if tokens[0] == "Total":
                                            eidx = len(e_bounds)-1
                                        elif tokens[0] == "1.000E+36":
                                            eidx = 0
                                        else:
                                            energy = float(tokens[0])
                                            eidx = calc_eidx(energy, e_bounds)
                                    elif items_count == 5:
                                        eidx = 0

                                    x = float(tokens[shift])
                                    y = float(tokens[shift+1])
                                    z = float(tokens[shift+2])
                                    result = float(tokens[shift+3])*multiplier
                                    error = float(tokens[shift+4])
                                    midx = calc_midx(
                                        [x, y, z], x_bounds, y_bounds, z_bounds)
                                    if midx in midxes_request:
                                        data[count] = (
                                            midx, eidx, result, error)
                                        count += 1
                            break
    return data


def extracted_results_to_table():
    """
    Extracts specified columns from an input CSV file, performs operations on them as defined in a configuration file,
    and saves the results to a new CSV file.

    The function reads a configuration file to determine the input and output file names, as well as the operations to
    perform on the extracted columns. It then loads the input CSV file into a DataFrame, extracts the specified columns,
    performs the operations, and saves the resulting DataFrame to the output CSV file.

    The configuration file should be in INI format and contain the following sections:
    - [general]: with keys 'input_file' and 'output_file' specifying the input and output CSV file names.
    - [operations]: with keys representing the names of the new columns to be created and values representing the
      operations to be performed on the extracted columns.

    The input CSV file should contain at least the columns 'Name', 'Coordinate', and 'Location', which will be included
    in the final output along with the calculated columns.

    Args:
        None

    Returns:
        None

    Raises:
        FileNotFoundError: If the input CSV file or configuration file does not exist.
        KeyError: If the configuration file does not contain the required sections or keys.
        pandas.errors.EmptyDataError: If the input CSV file is empty.
        pandas.errors.ParserError: If the input CSV file cannot be parsed.
        Exception: If any other error occurs during the execution of the operations.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=False, default='config.ini',
                        help="Configure file")
    args = vars(parser.parse_args())

    # Read the configuration file
    config = configparser.ConfigParser()
    config.read(args['config'])
    # Get the input and output file names from the configuration file
    input_file = config['general'].get('input_file', 'result.csv')
    output_file = config['general'].get(
        'output_file', 'result_with_operations.csv')

    # Extract all column names used in the operations
    columns_to_extract = set()
    for operation in config['operations'].values():
        columns_to_extract.update(re.findall(
            r'\b[A-Za-z_][A-Za-z0-9_.]*\b', operation))

    # Convert the set to a list
    columns_to_extract = list(columns_to_extract)

    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Extract the specified columns
    extracted_df = df[columns_to_extract]

    # Perform operations based on the configuration file
    for operation_name, operation in config['operations'].items():
        # Replace column names with DataFrame references
        for col in columns_to_extract:
            operation = operation.replace(col, f"extracted_df['{col}']")

        # Evaluate the operation
        extracted_df[operation_name] = eval(operation)

    # Include the columns "Name", "Coordinate", and "Location" in the final DataFrame
    final_df = df[['Name', 'Coordinate', 'Location']].join(extracted_df)

    # Keep only the 'Name', 'Coordinate', 'Location', and the calculated items with operations
    final_columns = ['Name', 'Coordinate', 'Location'] + \
        list(config['operations'].keys())
    # format the digits
    for col in final_columns:
        if col != 'Name' and col != 'Coordinate' and col != 'Location':
            final_df[col] = final_df[col].apply(
                lambda x: format_single_output(x, decimals=2))
    final_df = final_df[final_columns]

    # Save the new DataFrame with the results to a new CSV file
    final_df.to_csv(output_file, index=False)

    print(f"New CSV file with operations saved as '{output_file}'")


class MeshtalWithNumber(mcnp.Meshtal):
    """add extra parameter self.tally_number to only read the assigned part of output"""

    def __init__(self, filename, tags=None, meshes_have_mats=False, tally_number=None):
        if not HAVE_PYMOAB:
            raise RuntimeError(
                "PyMOAB is not available, " "unable to create Meshtal.")

        self.tally = {}
        self.tags = tags
        self._meshes_have_mats = meshes_have_mats
        self.tally_number = tally_number

        with open(filename, "r") as f:
            self._read_meshtal_head(f)
            self._read_tallies(f)

    def _read_tallies(self, f):
        """Read in all of the mesh tallies from the meshtal file."""
        line = f.readline()
        if self.tally_number is not None:
            flag = False  # flag is used to check whether there is assigned tally number in the output file
            while line != "":
                if line.split()[0:3] == ["Mesh", "Tally", "Number"] and self.tally_number == int(line.split()[3]):
                    flag = True
                    if self.tags is not None and self.tally_number in self.tags.keys():
                        self.tally[self.tally_number] = self.create_meshtally(
                            f,
                            self.tally_number,
                            self.tags[self.tally_number],
                            mesh_has_mats=self._meshes_have_mats,
                        )
                    else:
                        self.tally[self.tally_number] = self.create_meshtally(
                            f, self.tally_number, mesh_has_mats=self._meshes_have_mats
                        )
                    return
                else:
                    line = f.readline()
            if flag == False:
                raise LookupError(
                    f"tally_number {self.tally_number} doesn't exist in the output file")
        else:
            while line != "":
                if line.split()[0:3] == ["Mesh", "Tally", "Number"]:
                    tally_num = int(line.split()[3])
                    if self.tags is not None and tally_num in self.tags.keys():
                        self.tally[tally_num] = self.create_meshtally(
                            f,
                            tally_num,
                            self.tags[tally_num],
                            mesh_has_mats=self._meshes_have_mats,
                        )
                    else:
                        self.tally[tally_num] = self.create_meshtally(
                            f, tally_num, mesh_has_mats=self._meshes_have_mats
                        )

                line = f.readline()


def main():
    """
    Analysis the meshtally.
    """
    meshtal_analysis = (
        'This script read a meshtal file and analysis specific tally\n')
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--ctm", required=False,
                        help="Computer time used in minutes")
    parser.add_argument("-l", "--log", required=False,
                        help="Log file contains ctm")
    parser.add_argument("-f", "--filename", required=False,
                        help="Meshtal file, default: meshtal")
    parser.add_argument("-p", "--particle", required=False,
                        help="Particle type, allowed particle: n, p. default: n")
    parser.add_argument("-t", "--tally", required=False,
                        help="Tally number to analysis, default: 4")
    parser.add_argument("-m", "--multiplier", required=False,
                        help="Multiply the data to a value, default: 1.0")
    parser.add_argument("-r", "--position", nargs=3,
                        required=False, help="the coordinates to get the result")
    parser.add_argument("--pos_file", required=False,
                        help="Multiple positions to get the result")
    parser.add_argument("-pc", "--pos_config", required=False,
                        help="Config file contains positions and ids to get the result")
    parser.add_argument("--box_file", required=False,
                        help="The file defining AABB box of the interested range. One box per line. Define box by: xmin, ymin, zmin, xmax, ymax, zmax name(optional)")
    parser.add_argument("--angle_range", required=False,
                        help="Rotate the box/point to +- angle range")
    args = vars(parser.parse_args())

    verbose_string = 'meshtal_analysis.py'

    filename = 'meshtal'
    if args['filename'] is not None:
        filename = args['filename']
        print(f"meshtally will be read from {filename}")
        verbose_string = f"{verbose_string} -f {filename}"

    particle = 'n'
    if args['particle'] is not None:
        particle = args['particle']
        print(f"partile type of the problem {particle}")
        verbose_string = f"{verbose_string} -p {particle}"

    tally_ana = 4
    if args['tally'] is not None:
        tally_ana = int(args['tally'])
        print(f"tally {tally_ana} will be analyzed")
        verbose_string = f"{verbose_string} -t {tally_ana}"

    multiplier = 1.0
    if args['multiplier'] is not None:
        multiplier = float(args['multiplier'])
        print(f"tally results are multiplied by {multiplier}")
        verbose_string = f"{verbose_string} -m {args['multiplier']}"

    if args['log'] is not None:
        ctm = get_ctm(args['log'])
        print(f"ctm read from log file: {ctm}")
        verbose_string = f"{verbose_string} -l {args['log']}"

    ctm = None
    if args['ctm'] is not None:
        ctm = float(args['ctm'])  # in minutes
        print(f"ctm given and used is: {ctm}")
        verbose_string = f"{verbose_string} -c {args['ctm']}"

    position = None
    if args['position'] is not None:
        position = []
        for i in range(3):
            position.append(float(args['position'][i]))
        verbose_string = f"{verbose_string} -r {args['position'][0]} {args['position'][1]} {args['position'][2]}"

    pos_file = None
    if args['pos_file'] is not None:
        pos_file = args['pos_file']
        verbose_string = f"{verbose_string} --pos_file {pos_file}"
        print(f"positons will read from {pos_file}")

    pos_config = None
    if args['pos_config'] is not None:
        pos_config = args['pos_config']
        verbose_string = f"{verbose_string} --pos_config {pos_config}"
        print(f"parameters will read from {pos_config}")

    box_file = None
    if args['box_file'] is not None:
        box_file = args['box_file']
        verbose_string = f"{verbose_string} --box_file {box_file}"

    angle_range = 360
    if args['angle_range']:
        angle_range = float(args['angle_range'])
        verbose_string = f"{verbose_string} --angle_range {args['angle_range']}"

    if pos_config:
        get_result_by_config(pos_config)
        return  # skip normal analysis

    remove_tally_fc(filename)
    tally_nums = get_tally_nums(filename)
    print(f"tally numbers in the {filename}: {tally_nums}")
    tags = create_tags(tally_nums, particle=particle)
    print(f"tags for the {filename}: {tags}")
    meshtal = MeshtalWithNumber(filename, tags=tags, tally_number=tally_ana)
    # meshtal = mcnp.Meshtal(filename, tags=tags)
    meshtally = meshtal.tally[tally_ana]
    x_bounds = meshtally.x_bounds
    y_bounds = meshtally.y_bounds
    z_bounds = meshtally.z_bounds

    # multiply the multiplier
    meshtally = scale_with_multiplier(meshtally, multiplier, particle)

    # get result for specific position
    if position:
        get_result_by_pos(meshtally, position, particle=particle,
                          verbose_string=verbose_string)
        return  # skip normal analysis

    if pos_file:
        names, positions, locations = parse_positions(pos_file)
        get_result_by_positions(meshtally, names, positions, locations,
                                particle=particle, verbose_string=verbose_string)
        return  # skip normal analysis

    if box_file:
        boxes, names = parse_boxes(box_file)
        rotated_boxes = []
        if angle_range:
            for i, box in enumerate(boxes):
                rotated_boxes.append(rotate_box(box, angle_range))
        box_results = []  # min, max, average
        for i, box in enumerate(rotated_boxes):
            midxes = calc_midxes_in_box(box, x_bounds, y_bounds, z_bounds)
            values = []
            if len(midxes) > 0 and max(midxes) < meshtally.num_ves:
                values = get_value_by_midxes(meshtally, midxes)
            else:
                values = get_value_by_corner_center(
                    meshtally, boxes[i], angle_range=angle_range)
            box_results.append(
                (min(values), max(values), sum(values)/len(values)))
        with open(f"{box_file}.out", 'w') as fo:
            for i, box in enumerate(boxes):
                line = f"{names[i]}: {box[0]}, {box[1]}, {box[2]}, {box[3]}, {box[4]}, {box[5]}, min: {box_results[i][0]:.5e}, max: {box_results[i][1]:.5e}, ave:{box_results[i][2]:.5e}"
                fo.write(line+'\n')
            fo.write(f"# {verbose_string}")
        return  # skip normal analysis

    # common analysis
    meshtally2h5m(meshtally)
    eta, eta_eff_10, eta_eff_5, fom_g = meshtally_evaluation(
        meshtally, ctm=ctm, tag_name=f'{particle}_total_rel_error')
    print(f"score percentage: eta:", eta)
    print(f"effective (<0.1) score percentage: eta_eff_10:", eta_eff_10)
    print(f"effective (<0.05) score percentage: eta_eff_5:", eta_eff_5)
    if ctm is not None:
        print(f"Global Figure-of-Merit, fom_g:", fom_g)
    plot_pdf_vs_rel_err(meshtally, f'{particle}_total_rel_error')
    plot_cdf_vs_rel_err(meshtally, f'{particle}_total_rel_error')


if __name__ == '__main__':
    main()
