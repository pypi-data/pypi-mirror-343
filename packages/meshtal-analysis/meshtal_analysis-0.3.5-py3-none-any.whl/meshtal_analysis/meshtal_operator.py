#!/usr/bin/python3
##############################################################################
# Author: Xiaokang Zhang, Zhiqi Shi
# Function: Adding two meshtallies with the same shape.
# Aim: adding nuclear responses from neutron and photon
#   - nuclear heat from n and p
#   - operation dose from n and p
# Usage:
#   - fill out the 'config.ini'
#   - run 'python3 meshtal_operate.py -h' for detailed information
# Changelog:
#   - 20240126: read assigned meshtally from meshtal
#   - 20221007: init the script
##############################################################################
import os
import numpy as np
import argparse
from pyne import mcnp
from pyne.mesh import MeshTally
import matplotlib.pyplot as plt
import seaborn as sns
from natf.utils import format_single_output
from meshtal_analysis.meshtal_analysis import MeshtalWithNumber
from pymoab import core as mb_core
from configparser import ConfigParser
import math


def relative_error_sum(a, rel_a, b, rel_b):
    """
    Calculate the relative error of a + b.

    Parameters:
    - a: float, value of a
    - rel_a: float, relative error of a
    - b: float, value of b
    - rel_b: float, relative error of b

    Returns:
    - rel_a_plus_b: float, relative error of a + b
    """
    if a + b == 0:
        raise ValueError(
            "Sum of a and b cannot be zero when calculating relative error.")

    abs_error_a = a * rel_a
    abs_error_b = b * rel_b
    combined_abs_error = math.sqrt(abs_error_a**2 + abs_error_b**2)
    rel_a_plus_b = combined_abs_error / (a + b)
    return rel_a_plus_b


def relative_error_sum_arrays(a, rel_a, b, rel_b):
    """
    Calculate the relative error of a + b for NumPy arrays.

    Parameters:
    - a: np.ndarray, values of a
    - rel_a: np.ndarray, relative errors of a
    - b: np.ndarray, values of b
    - rel_b: np.ndarray, relative errors of b

    Returns:
    - rel_a_plus_b: np.ndarray, relative errors of a + b
    Calculate the relative error of a + b.
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        # Calculate absolute errors
        abs_error_a = a * rel_a
        abs_error_b = b * rel_b

        # Calculate combined absolute error
        combined_abs_error = np.sqrt(abs_error_a**2 + abs_error_b**2)

        # Calculate relative error of the sum
        rel_a_plus_b = np.where(a + b != 0, combined_abs_error / (a + b), 0)
        return rel_a_plus_b


def relative_error_difference(a, rel_a, b, rel_b):
    """
    Calculate the relative error of a - b.

    Parameters:
    - a: float, value of a
    - rel_a: float, relative error of a
    - b: float, value of b
    - rel_b: float, relative error of b

    Returns:
    - rel_a_minus_b: float, relative error of a - b
    """
    if a == b:
        raise ValueError(
            "The difference a - b cannot be zero when calculating relative error.")

    abs_error_a = a * rel_a
    abs_error_b = b * rel_b
    combined_abs_error = math.sqrt(abs_error_a**2 + abs_error_b**2)
    rel_a_minus_b = combined_abs_error / abs(a - b)
    return rel_a_minus_b


def relative_error_difference_arrays(a, rel_a, b, rel_b):
    """
    Calculate the relative error of a - b for NumPy arrays.

    Parameters:
    - a: np.ndarray, values of a
    - rel_a: np.ndarray, relative errors of a
    - b: np.ndarray, values of b
    - rel_b: np.ndarray, relative errors of b

    Returns:
    - rel_a_minus_b: np.ndarray, relative errors of a - b
    Calculate the relative error of a - b.
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        # Calculate absolute errors
        abs_error_a = a * rel_a
        abs_error_b = b * rel_b

        # Calculate combined absolute error
        combined_abs_error = np.sqrt(abs_error_a**2 + abs_error_b**2)

        # Calculate relative error of the difference
        rel_a_minus_b = np.where(a - b != 0, combined_abs_error / (a - b), 0)
        return rel_a_minus_b


def relative_error_product(rel_a, rel_b):
    """
    Calculate the relative error of a * b.

    Parameters:
    - rel_a: float, relative error of a
    - rel_b: float, relative error of b

    Returns:
    - rel_a_times_b: float, relative error of a * b
    """
    rel_a_times_b = math.sqrt(rel_a**2 + rel_b**2)
    return rel_a_times_b


def relative_error_product_arrays(rel_a, rel_b):
    """
    Calculate the relative error of a * b for NumPy arrays.

    Parameters:
    - a: np.ndarray, values of a
    - rel_a: np.ndarray, relative errors of a
    - b: np.ndarray, values of b
    - rel_b: np.ndarray, relative errors of b

    Returns:
    - rel_a_times_b: np.ndarray, relative errors of a * b
    Calculate the relative error of a * b.
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        # Calculate combined absolute error
        rel_a_times_b = np.sqrt(np.power(rel_a, 2) + np.power(rel_b, 2))
        return rel_a_times_b


def relative_error_division(rel_a, rel_b):
    """
    Calculate the relative error of a / b.

    Parameters:
    - rel_a: float, relative error of a
    - rel_b: float, relative error of b

    Returns:
    - rel_a_div_b: float, relative error of a / b
    """
    rel_a_div_b = math.sqrt(rel_a**2 + rel_b**2)
    return rel_a_div_b


def relative_error_division_arrays(rel_a, rel_b):
    """
    Calculate the relative error of a / b for NumPy arrays.

    Parameters:
    - a: np.ndarray, values of a
    - rel_a: np.ndarray, relative errors of a
    - b: np.ndarray, values of b
    - rel_b: np.ndarray, relative errors of b

    Returns:
    - rel_a_div_b: np.ndarray, relative errors of a / b
    Calculate the relative error of a / b.
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        # Calculate combined absolute error
        rel_a_div_b = np.sqrt(np.power(rel_a, 2) + np.power(rel_b, 2))
        return rel_a_div_b


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


def meshtally2h5m(meshtally, ofname=None):
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
    if ofname is None:
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
    meshtally1 = meshtally
    ptype = get_ptype(particle)
    # result
    result_tag_name = f"{ptype}_result"
    result = getattr(meshtally1, result_tag_name)[:]
    result = np.multiply(result, multiplier)
    if ptype == 'n':
        meshtally1.n_result[:] = result[:]
    elif ptype == 'p':
        meshtally1.p_result[:] = result[:]
    # total result
    total_result_tag_name = f"{ptype}_total_result"
    total_result = getattr(meshtally1, total_result_tag_name)[:]
    total_result = np.multiply(total_result, multiplier)
    if ptype == 'n':
        meshtally1.n_total_result[:] = total_result[:]
    elif ptype == 'p':
        meshtally1.p_total_result[:] = total_result[:]
    return meshtally1


def add_meshtally_results(meshtally1, meshtally2, calc_group=False, calc_rel_err=False):
    """Add two meshtallies"""
    meshtally = meshtally1
    particle = 'n'
    print(f"Adding n_result of meshtally1 and meshtally2 ...")
    if calc_group:
        # add result
        result1 = meshtally1.n_result[:]
        result2 = meshtally2.n_result[:]
        result = np.add(result1, result2)
        meshtally.n_result[:] = result[:]
        if calc_rel_err:
            # add rel_err
            rel_err1 = meshtally1.n_rel_error[:]
            rel_err2 = meshtally2.n_rel_error[:]
            rel_err = relative_error_sum_arrays(
                result1, rel_err1, result2, rel_err2)
            meshtally.n_rel_error[:] = rel_err[:]
    # add total result
    result1 = meshtally1.n_total_result[:]
    result2 = meshtally2.n_total_result[:]
    result = np.add(result1, result2)
    meshtally.n_total_result[:] = result[:]
    if calc_rel_err:
        # add total rel_err
        rel_err1 = meshtally1.n_total_rel_error[:]
        rel_err2 = meshtally2.n_total_rel_error[:]
        rel_err = relative_error_sum_arrays(
            result1, rel_err1, result2, rel_err2)
        meshtally.n_total_rel_error[:] = rel_err[:]
    return meshtally


def multiply_meshtally_results(meshtally1, meshtally2, calc_group=False, calc_rel_err=False):
    """Multiply two meshtallies element-wise."""
    meshtally = meshtally1
    # multiply result
    if calc_group:
        # multiply result
        result1 = meshtally1.n_result[:]
        result2 = meshtally2.n_result[:]
        result = np.multiply(result1, result2)
        meshtally.n_result[:] = result[:]
        if calc_rel_err:
            # multiply rel_err
            rel_err1 = meshtally1.n_rel_error[:]
            rel_err2 = meshtally2.n_rel_error[:]
            rel_err = relative_error_product_arrays(
                rel_err1, rel_err2)
            meshtally.n_rel_error[:] = rel_err[:]

    # multiply total result
    result1 = meshtally1.n_total_result[:]
    result2 = meshtally2.n_total_result[:]
    result = np.multiply(result1, result2)
    meshtally.n_total_result[:] = result[:]
    if calc_rel_err:
        # multiply total rel_err
        rel_err1 = meshtally1.n_total_rel_error[:]
        rel_err2 = meshtally2.n_total_rel_error[:]
        rel_err = relative_error_product_arrays(
            rel_err1, rel_err2)
        meshtally.n_total_rel_error[:] = rel_err[:]
    return meshtally


def divide_meshtally_results(meshtally1, meshtally2, calc_group=False, calc_rel_err=False):
    """Divide two meshtallies element-wise."""
    if calc_group:
        # divide result
        result1 = meshtally1.n_result[:]
        result2 = meshtally2.n_result[:]
        result = np.divide(result1, result2, where=result2 != 0)
        meshtally1.n_result[:] = result[:]
        if calc_rel_err:
            rel_err1 = meshtally1.n_rel_error[:]
            rel_err2 = meshtally2.n_rel_error[:]
            rel_err = relative_error_division_arrays(
                rel_err1, rel_err2)
            meshtally1.n_rel_error[:] = rel_err[:]
    # divide total result
    result1 = meshtally1.n_total_result[:]
    result2 = meshtally2.n_total_result[:]
    result = np.divide(result1, result2, where=result2 != 0)
    meshtally1.n_total_result[:] = result[:]
    if calc_rel_err:
        # divide total rel_err
        rel_err1 = meshtally1.n_total_rel_error[:]
        rel_err2 = meshtally2.n_total_rel_error[:]
        rel_err = relative_error_division_arrays(
            rel_err1, rel_err2)
        meshtally1.n_total_rel_error[:] = rel_err[:]
    return meshtally1


def calc_midx(r, x_bounds, y_bounds, z_bounds):
    """
    Calculate the index of the mesh element.
    """
    xidx = np.searchsorted(x_bounds, r[0]) - 1
    yidx = np.searchsorted(y_bounds, r[1]) - 1
    zidx = np.searchsorted(z_bounds, r[2]) - 1
    midx = zidx + yidx*(len(z_bounds)-1) + xidx * \
        (len(y_bounds)-1)*(len(z_bounds)-1)
    return midx


def get_result_by_pos(meshtally, r, particle='n', ofname='result.txt', style='fispact'):
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
        else:
            raise ValueError(f"style {style} not supported")
    fo.close()


def get_meshtally(filename, particle, tally_ana):
    if filename.split('.')[-1] == 'h5m':
        meshtally = MeshTally()
        meshtally.mesh = mb_core.Core()
        meshtally.mesh.load_file(filename)
        super(MeshTally, meshtally).__init__(
            mesh=meshtally.mesh, structured=True)
        return meshtally
    else:
        remove_tally_fc(filename)
        tags = create_tags(tally_ana, particle=particle)
        meshtal = MeshtalWithNumber(
            filename, tags=tags, tally_number=tally_ana)
        meshtally = meshtal.tally[tally_ana]
        return meshtally


def main():
    """
    Operate the meshtally in meshtals or initialize a config.ini file.
    """
    meshtal_analysis = (
        'This script reads meshtal files and operates the meshtally results.\n')
    parser = argparse.ArgumentParser(description=meshtal_analysis)
    parser.add_argument("-c", "--config", required=False, default="config.ini",
                        help="Specify the config file (default: config.ini)")
    parser.add_argument("--setup", action="store_true",
                        help="Initialize a config.ini file for user modification")
    args = vars(parser.parse_args())

    if args["setup"]:
        # Initialize a config.ini file
        config_content = """[meshtally1]
filename = meshtal1
tallyid = 4
multiplier = 1.0
calc_group = False
calc_rel_err = False
output = result

[meshtally2]
filename = meshtal2
tallyid = 4
multiplier = 1.0
operator = add
"""
        with open("config.ini", "w") as config_file:
            config_file.write(config_content)
        print("config.ini file has been created. Please modify it as needed.")
        return

    # Proceed with the normal operation
    conf = ConfigParser()
    conf.read(args['config'])
    meshtallys = conf.sections()
    print(f'getting {meshtallys[0]} ...')
    particle = 'n'
    meshtally1 = get_meshtally(
        conf[meshtallys[0]]['filename'], 'n', conf[meshtallys[0]].getint('tallyid'))
    calc_group = False
    calc_rel_err = False
    try:
        calc_group = conf[meshtallys[0]].getboolean('calc_group')
    except:
        pass
    try:
        calc_rel_err = conf[meshtallys[0]].getboolean('calc_rel_err')
    except:
        pass
    ofname = "result.h5m"
    try:
        ofname = conf[meshtallys[0]]['output']
        if 'h5m' not in ofname:
            ofname = ofname + '.h5m'
    except:
        pass
    meshtally1 = scale_with_multiplier(
        meshtally1, conf[meshtallys[0]].getfloat('multiplier'), 'n')
    operator = 'add'
    for i, tally in enumerate(meshtallys[1:]):
        print(f'getting {tally} ...')
        meshtally2 = get_meshtally(
            conf[tally]['filename'], 'n', conf[tally].getint('tallyid'))
        operator = conf[tally]['operator']
        multiplier2 = float(conf[tally]['multiplier'])
        if operator.lower() == 'add':
            print(f"  adding meshtally1 and meshtally2 ...")
            meshtally2 = scale_with_multiplier(
                meshtally2, multiplier2, particle)
            meshtally1 = add_meshtally_results(
                meshtally1, meshtally2, calc_group=calc_group, calc_rel_err=calc_rel_err)
        elif operator.lower() in ('sub', 'subtract'):
            print(f"  subtracting meshtally1 by meshtally2 ...")
            meshtally2 = scale_with_multiplier(
                meshtally2, -multiplier2, particle)
            meshtally1 = add_meshtally_results(
                meshtally1, meshtally2, calc_group=calc_group, calc_rel_err=calc_rel_err)
        elif operator.lower() == 'mul':
            print(f"  multiplying meshtally1 and meshtally2 element-wise ...")
            meshtally2 = scale_with_multiplier(
                meshtally2, multiplier2, particle)
            meshtally1 = multiply_meshtally_results(
                meshtally1, meshtally2, calc_group=calc_group, calc_rel_err=calc_rel_err)
        elif operator.lower() in ('div', 'divide'):
            print(f"  dividing meshtally1 by meshtally2 element-wise ...")
            meshtally2 = scale_with_multiplier(
                meshtally2, multiplier2, particle)
            meshtally1 = divide_meshtally_results(
                meshtally1, meshtally2, calc_group=calc_group, calc_rel_err=calc_rel_err)
        else:
            raise ValueError(
                f"Unsupported operator '{operator}'. Supported operators: 'add', 'sub', 'subtract', 'mul', 'div', 'divide'.")
    print(f"writing results...")
    meshtally2h5m(meshtally1, ofname=ofname)
    print(f"Done")


if __name__ == '__main__':
    main()
