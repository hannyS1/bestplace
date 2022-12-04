import h3


def main():
    print(h3.geo_to_h3(37.525369, 55.531259, 11))
    print(h3.h3_to_geo("8b2cce883b5dfff"))
    print(h3.k_ring("8b2cce883b5dfff", 1))


if __name__ == "__main__":
    main()
