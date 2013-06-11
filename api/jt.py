import glance

def get_image_quota(project_id):
    import subprocess
    cmd = 'sudo /root/novac/bin/novac quota-image-get %s' % project_id
    image_limit = subprocess.check_output(cmd, shell=True)
    return int(image_limit.strip())

def set_image_quota(project_id, quota):
    import subprocess
    cmd = 'sudo /root/novac/bin/novac quota-image-set %s %s' % (project_id, quota)
    subprocess.check_call(cmd, shell=True)

def get_image_count(project_id, request):
    (all_images, more_images) = glance.image_list_detailed(request)
    images = [im for im in all_images if im.owner == project_id]
    return len(images)

def get_object_mb_quota(project_id):
    import subprocess
    cmd = 'sudo /root/novac/bin/novac quota-object_mb-get %s' % project_id
    object_mb = subprocess.check_output(cmd, shell=True)
    return int(object_mb.strip())

def set_object_mb_quota(project_id, quota):
    import subprocess
    cmd = 'sudo /root/novac/bin/novac quota-object_mb-set %s %s' % (project_id, quota)
    subprocess.check_call(cmd, shell=True)

def get_object_mb_usage(project_id):
    import subprocess
    cmd = 'sudo /root/novac/bin/novac quota-object_mb-usage %s' % project_id
    object_mb_usage = subprocess.check_output(cmd, shell=True)
    return int(object_mb_usage.strip())

def get_expiration_dates():
    dates = {}
    with open('/etc/openstack-dashboard/dair-expiration.txt') as f:
        for line in f:
            line = line.strip()
            if line != "":
                foo = line.split(':')
                dates[foo[0]] = foo[1]
    return dates

def get_expiration_date(project_id):
    dates = get_expiration_dates()
    if project_id in dates:
        return dates[project_id]
    else:
        return "Information not available."

def set_expiration_date(project_id, expiration_date):
    dates = get_expiration_dates()
    dates[project_id] = expiration_date
    with open('/etc/openstack-dashboard/dair-expiration.txt', 'w') as f:
        for k, v in dates.iteritems():
            f.write("%s:%s\n" % (k,v))
