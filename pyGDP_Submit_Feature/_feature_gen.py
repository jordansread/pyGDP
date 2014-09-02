def _generateFeatureRequest(self, typename, attribute=None):
    """
    This function, given a attribute and a typename or filename will return a list of values associated
    with the file and the attribute chosen.
    """
    
    service_url = WFS_URL
    qs = []
    if service_url.find('?') != -1:
            qs = cgi.parse_qsl(service_url.split('?')[1])

    params = [x[0] for x in qs]

    if 'service' not in params:
        qs.append(('service', 'WFS'))
    if 'request' not in params:
        if attribute is None:
            qs.append(('request', 'DescribeFeatureType'))
        else:
            qs.append(('request', 'GetFeature'))
    if 'version' not in params:
        qs.append(('version', '1.1.0'))
    if 'typename' not in params:
        qs.append(('typename', typename))
    if attribute is not None:
        if 'propertyname' not in params:
            qs.append(('propertyname', attribute))
        
    urlqs = urlencode(tuple(qs))
    return service_url.split('?')[0] + '?' + urlqs
