import dirstatstocloudwatch.util as util


def test_get_objects_in_folder_count():
    num_objects = util.get_folder_object_info(folder_name='data/', get_object_count=True, get_total_bytes=False)['object_count']
    assert num_objects == 8

def test_get_objects_in_folder_bytes():
    total_bytes = util.get_folder_object_info(folder_name='data/', get_object_count=False, get_total_bytes=True)['total_bytes']
    assert total_bytes == 89

def test_get_objects_in_folder_both():
    results = util.get_folder_object_info(folder_name='data/', get_object_count=True, get_total_bytes=True)
    assert results['total_bytes'] == 89
    assert results['object_count'] == 8