import gdsfactory as gf

from hhi import cells, tech


@gf.cell
def sample_route_bundle_gsg():
    c = gf.Component()
    d1 = c << cells.HHI_DFB()

    p1 = c << cells.pad()
    p1.movey(250)
    # _ = tech.route_bundle_gsg(c, [d1.ports["g1"]], [p1.ports["e1"]])
    _ = tech.route_bundle_sbend_dc(
        c,
        [d1.ports["g1"]],
        [p1.ports["e1"]],
        use_port_width=True,
        allow_type_mismatch=True,
    )
    return c


if __name__ == "__main__":
    c = sample_route_bundle_gsg()
    c.show()
