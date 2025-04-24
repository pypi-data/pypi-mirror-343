import inspect

import gdsfactory as gf

from hhi import cells
from hhi.cells.fixed import (
    HHI_BPD,
    HHI_DBR,
    HHI_DFB,
    HHI_EAM,
    HHI_GRAT,
    HHI_MIR1E1700,
    HHI_MIR2E1700,
    HHI_MZMDD,
    HHI_MZMDU,
    HHI_PDDC,
    HHI_PMTOE200,
    HHI_PMTOE600,
    HHI_PMTOE1700,
    HHI_R50GSG,
    HHI_SGDBRTO,
    HHI_SOA,
    HHI_SSCLATE200,
    HHI_SSCLATE1700,
    HHI_WGTE200E600,
    HHI_WGTE200E1700,
    HHI_WGTE600E1700,
    HHI_BJsingle,
    HHI_BJtwin,
    HHI_DBRsection,
    HHI_DFBsection,
    HHI_DirCoupE600,
    HHI_DirCoupE1700,
    HHI_EAMsection,
    HHI_EOBiasSectionSingle,
    HHI_EOBiasSectionTwin,
    HHI_EOElectricalGND,
    HHI_EOPMTermination,
    HHI_EOPMTWSingleDD,
    HHI_EOPMTWSingleDU,
    HHI_EOPMTWTwinDD,
    HHI_EOPMTWTwinDU,
    HHI_FacetWGE200,
    HHI_FacetWGE600,
    HHI_FacetWGE1700,
    HHI_FacetWGE1700twin,
    HHI_GRATsection,
    HHI_GSGtoGS,
    HHI_ISOsectionSingle,
    HHI_ISOsectionTwin,
    HHI_METMETx,
    HHI_MMI1x2ACT,
    HHI_MMI1x2E600,
    HHI_MMI1x2E1700,
    HHI_MMI2x2ACT,
    HHI_MMI2x2E600,
    HHI_MMI2x2E1700,
    HHI_MZIswitch,
    HHI_PDRFsingle,
    HHI_PDRFtwin,
    HHI_PolConverter45,
    HHI_PolConverter90,
    HHI_PolSplitter,
    HHI_SOAsection,
    HHI_TOBiasSection,
    HHI_WGMETxACTGSGsingle,
    HHI_WGMETxACTGSGtwin,
    HHI_WGMETxACTGSsingle,
    HHI_WGMETxACTGStwin,
    HHI_WGMETxACTsingle,
    HHI_WGMETxACTtwin,
    HHI_WGMETxE200,
    HHI_WGMETxE200GS,
    HHI_WGMETxE200GSG,
    HHI_WGMETxE600,
    HHI_WGMETxE600GS,
    HHI_WGMETxE600GSG,
    HHI_WGMETxE1700GSGsingle,
    HHI_WGMETxE1700GSGtwin,
    HHI_WGMETxE1700GSsingle,
    HHI_WGMETxE1700GStwin,
    HHI_WGMETxE1700single,
    HHI_WGMETxE1700twin,
)
from hhi.config import PATH

size1 = (2e3, 8e3)
size2 = (4e3, 8e3)
size3 = (12e3, 8e3)


def run_with_defaults_and_doubles(functions):
    results = []
    for fn in functions:
        sig = inspect.signature(fn)

        # Collect default parameters
        default_kwargs = {
            k: v.default
            for k, v in sig.parameters.items()
            if v.default is not inspect.Parameter.empty
        }

        # Compute doubled parameters
        doubled_kwargs = {
            k: v * 2 if isinstance(v, int | float) else v
            for k, v in default_kwargs.items()
        }

        # Call function with default and doubled
        result_default = fn(**default_kwargs)
        result_doubled = fn(**doubled_kwargs)
        results.append(result_default)
        results.append(result_doubled)

    return results


@gf.cell
def sample_all_cells_with_variations() -> gf.Component:
    """Returns a sample die."""
    c = gf.Component()

    components = [
        HHI_BJsingle,
        HHI_BJtwin,
        HHI_BPD,
        HHI_DBR,
        HHI_DBRsection,
        HHI_DFB,
        HHI_DFBsection,
        HHI_DirCoupE1700,
        HHI_DirCoupE600,
        HHI_EAM,
        HHI_EAMsection,
        HHI_EOBiasSectionSingle,
        HHI_EOBiasSectionTwin,
        HHI_EOElectricalGND,
        HHI_EOPMTWSingleDD,
        HHI_EOPMTWSingleDU,
        HHI_EOPMTWTwinDD,
        HHI_EOPMTWTwinDU,
        HHI_EOPMTermination,
        HHI_FacetWGE1700,
        HHI_FacetWGE1700twin,
        HHI_FacetWGE200,
        HHI_FacetWGE600,
        HHI_GRAT,
        HHI_GRATsection,
        HHI_GSGtoGS,
        HHI_ISOsectionSingle,
        HHI_ISOsectionTwin,
        HHI_METMETx,
        HHI_MIR1E1700,
        HHI_MIR2E1700,
        HHI_MMI1x2ACT,
        HHI_MMI1x2E1700,
        HHI_MMI1x2E600,
        HHI_MMI2x2ACT,
        HHI_MMI2x2E1700,
        HHI_MMI2x2E600,
        HHI_MZIswitch,
        HHI_MZMDD,
        HHI_MZMDU,
        HHI_PDDC,
        HHI_PDRFsingle,
        HHI_PDRFtwin,
        HHI_PMTOE1700,
        HHI_PMTOE200,
        HHI_PMTOE600,
        HHI_PolConverter45,
        HHI_PolConverter90,
        HHI_PolSplitter,
        HHI_R50GSG,
        HHI_SGDBRTO,
        HHI_SOA,
        HHI_SOAsection,
        HHI_SSCLATE1700,
        HHI_SSCLATE200,
        HHI_TOBiasSection,
        HHI_WGMETxACTGSGsingle,
        HHI_WGMETxACTGSGtwin,
        HHI_WGMETxACTGSsingle,
        HHI_WGMETxACTGStwin,
        HHI_WGMETxACTsingle,
        HHI_WGMETxACTtwin,
        HHI_WGMETxE1700GSGsingle,
        HHI_WGMETxE1700GSGtwin,
        HHI_WGMETxE1700GSsingle,
        HHI_WGMETxE1700GStwin,
        HHI_WGMETxE1700single,
        HHI_WGMETxE1700twin,
        HHI_WGMETxE200,
        HHI_WGMETxE200GS,
        HHI_WGMETxE200GSG,
        HHI_WGMETxE600,
        HHI_WGMETxE600GS,
        HHI_WGMETxE600GSG,
        HHI_WGTE200E1700,
        HHI_WGTE200E600,
        HHI_WGTE600E1700,
    ]

    print(f"Number of components: {len(components)}")

    components = run_with_defaults_and_doubles(components)

    print(f"Number of components: {len(components)}")

    components += [
        cells.die,
        cells.cleave_mark,
        cells.pad,
        cells.die_rf,
    ]

    c = gf.pack(components, spacing=20)[0]
    # c = gf.grid(components, shape=(2, 2))
    return c


if __name__ == "__main__":
    c = sample_all_cells_with_variations()
    c.write_gds(
        gdspath=PATH.home / "Downloads" / "hhi_all_cells.gds", with_metadata=False
    )
    c.show()
