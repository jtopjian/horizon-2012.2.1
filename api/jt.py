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
