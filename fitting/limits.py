import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import re
import uproot
import glob
import yaml
import matplotlib
print("Using backend:", matplotlib.get_backend())
np.seterr(divide='ignore', invalid='ignore')

if os.path.exists("physics.mplstyle"):
    plt.style.use("physics.mplstyle")
else:
    print("No style")
    
def get_limits(fn):
    try:
        f = uproot.open(fn)
        arrs = f["limit"].arrays(["limit", "quantileExpected"])
        limit = np.array(arrs["limit"])
        quant = np.array(arrs["quantileExpected"])
        print(f"{fn}: limit.shape = {limit.shape}, quant.shape = {quant.shape}")

        if len(limit) == 6 and len(quant) == 6:
            out = np.stack([quant, limit])
            print(f" -> stacked shape: {out.shape}")
            return out
        else:
            print(" -> Skipping: not enough entries")
            return -1
    except Exception as e:
        print(f"Error reading {fn}: {e}")
        return -1

    
def mass_points(kind="Scalar"):
    """Get DM mass points from ROOT file names."""
    mass_points = {}
    for p in glob.glob(f"./fitroom/higgsCombineDMSimp_*{kind}*"):
        mass_points[p] = [int(s) for s in re.findall(r'\d+', p)[:-1]]
    return mass_points

def get_cross_section(file):
    """Extract cross section from YAML config."""
    name = os.path.basename(file)
    with open("./config/xsection-DM.yaml", 'r') as stream:
        xsecs = yaml.safe_load(stream)
    name = name.replace("higgsCombine", "")
    name = name.replace(".AsymptoticLimits.mH125.root", "")
    xsec = xsecs[name]
    return xsec.get("xsec") * xsec.get("br") * xsec.get("kr")
cross_section_value = get_cross_section("./fitroom/higgsCombineDMSimp_MonoZLL_Scalar_10_mxd-1.AsymptoticLimits.mH125.root")
print("cross section times Br time Kr",cross_section_value)


def plot_Scalar(unblind=True, preliminary=False):
    """Plot 95% CL upper limits on cross-section ratio for Scalar mediator."""
    limit_MY = []
    limit_mx = []
    limit_lm = []
    xsec = []

    #for fn, mp in mass_points("Scalar").items():
    for fn, mp in mass_points("Pseudo").items():
        limit = get_limits(fn)
        if isinstance(limit, np.ndarray) and limit.shape == (2, 6):
            xsec.append(get_cross_section(fn))
            limit = np.array(limit).astype(float)
            limit_lm.append(limit)
            limit_MY.append(mp[0])
            limit_mx.append(mp[1])
        else:
            print("Skipping file (bad format):", fn)

    xsec = np.array(xsec)
    data = pd.DataFrame({
        "obs": 0.02 * np.array(limit_lm)[:, 1, 5] / xsec,
        "exp": 0.02 * np.array(limit_lm)[:, 1, 2] / xsec,
        "m1s": 0.02 * np.array(limit_lm)[:, 1, 1] / xsec,
        "p1s": 0.02 * np.array(limit_lm)[:, 1, 3] / xsec,
        "m2s": 0.02 * np.array(limit_lm)[:, 1, 0] / xsec,
        "p2s": 0.02 * np.array(limit_lm)[:, 1, 4] / xsec,
        "MY": np.array(limit_MY)
    })
    print(data.to_string(index=False))
    data = data.sort_values(by=['MY'])
    plt.figure(figsize=(6.2, 6))
    ax = plt.gca()
    ax.fill_between(data.MY, data.m2s, data.p2s, color="#FFCC01", lw=0, label="95% expected")  # Yellow
    ax.fill_between(data.MY, data.m1s, data.p1s, color="#00CC00", lw=0, label="68% expected")  # Green
    ax.plot(data.MY, data.exp, marker='', linestyle="--", color="blue", label="Median expected")
    if unblind:
        ax.plot(data.MY, data.obs, marker='', linestyle="-", color="black", label="Observed")

    ax.axhline(1, ls="--", color="red")
    ax.set_xlabel(r"$m_{\rm med}$ [GeV]", fontsize=14)
    ax.set_ylabel(r"$95\%$ CL limit on $\sigma_{obs}/\sigma_{theo}$", fontsize=14)
    ax.set_xlim([min(data.MY) - 10, max(data.MY) + 10])
    ax.set_ylim([0.1, 1e4])
    ax.set_yscale("log")
    ax.text(0.05, 0.9, "CMS $\it{Preliminary}$" if preliminary else "CMS", transform=ax.transAxes,
            fontsize=18, fontweight='bold')
    ax.text(1.0, 1.0, r"137 fb$^{-1}$ (13 TeV)", transform=ax.transAxes,
            fontsize=14, ha='right', va='bottom')
    #ax.text(0.02, 0.1, r"Scalar mediator, $g_q = 1$", transform=ax.transAxes,
    ax.text(0.02, 0.1, r"Pseudo mediator, $g_q = 1$", transform=ax.transAxes,        
            fontsize=14, ha='left', va='bottom')
    ax.text(0.02, 0.05, r"Dirac DM, $m_{\chi} = 1$ GeV, $g_{\chi} = 1$", transform=ax.transAxes,
            fontsize=14, ha='left', va='bottom')

    ax.legend(loc="upper right", fontsize=12)
    plt.tight_layout()
    tag = "-preliminary" if preliminary else ""
    plt.savefig(f"limit-DM-pseudoscalar-model{tag}-big-CMS.pdf", bbox_inches='tight')
    plt.savefig(f"limit-DM-pseudoscalar-model{tag}-big-CMS.png", bbox_inches='tight')
    print("Plots saved: PNG and PDF.")


if __name__ == "__main__":
    print("Extracting mass points...")
    points = mass_points(kind="Scalar")
    print(points)

    plot_Scalar(preliminary=True)  
