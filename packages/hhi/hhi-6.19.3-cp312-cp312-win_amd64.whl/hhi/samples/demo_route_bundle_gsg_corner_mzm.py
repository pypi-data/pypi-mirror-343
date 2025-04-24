import gdsfactory as gf

from hhi import cells, tech


@gf.cell
def sample_route_bundle_sbend_gs():
    """FIXME: this is a sample route bundle with a gs corner."""
    c = gf.Component()
    d1 = c << cells.HHI_MZMDU()

    p1 = c << cells.pad()
    p1.center = d1.ports["s2"].center
    p1.movey(250)
    _ = tech.route_bundle_sbend_dc(
        c,
        [d1.ports["s2"]],
        [p1.ports["e1"]],
        use_port_width=True,
        allow_type_mismatch=True,
    )
    return c


if __name__ == "__main__":
    c = sample_route_bundle_sbend_gs()
    c.show()
