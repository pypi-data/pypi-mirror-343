import gdsfactory as gf

from hhi import cells, tech


@gf.cell
def sample_route_bundle_gs():
    """sample route bundle with mzm.

    fixme: this should be a test

    """
    c = gf.Component()
    m1 = c << cells.HHI_MZMDU()

    p1 = c << cells.pad_GS()
    p1.rotate(90)
    p1.center = m1.ports["s2"].center
    p1.movey(2000)
    p1.movex(200)
    _ = tech.route_bundle_gs(c, [m1.ports["s2"]], [p1.ports["e1"]])
    return c


@gf.cell
def sample_route_bundle_sbend_gs():
    """Sample route bundle with MZM."""
    c = gf.Component()
    m1 = c << cells.HHI_MZMDU()

    p1 = c << cells.pad_GS()
    p1.rotate(90)
    p1.center = m1.ports["s2"].center
    p1.movey(800)
    p1.movex(50)
    _ = tech.route_bundle_sbend_gs(
        c,
        [m1.ports["s2"]],
        [p1.ports["e1"]],
        cross_section="GS",
    )
    return c


if __name__ == "__main__":
    c = sample_route_bundle_gs()
    c.show()
