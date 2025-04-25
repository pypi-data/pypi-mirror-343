import tonic


def test_read_aedat_header():
    data_version, data_start, start_timestamp = tonic.io.read_aedat_header_from_file(
        "test/test_data/sample_aedat_header.aedat"
    )

    assert data_version == 2
    assert start_timestamp == 1695355587880


def test_read_aedat_events():
    data_version, data_start, start_timestamp = tonic.io.read_aedat_header_from_file(
        "test/test_data/sample.aedat4"
    )
    events = tonic.io.get_aer_events_from_file(
        "test/test_data/sample.aedat4", data_version, data_start
    )
    assert len(events) == 118651


def test_read_aedat4():
    events = tonic.io.read_aedat4("test/test_data/sample.aedat4")
