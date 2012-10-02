from django.conf import settings

# This is disabled on pypi.python.org, can be useful if you make mistakes
if not hasattr(settings,'DJANGOPYPI_ALLOW_VERSION_OVERWRITE'):
    settings.DJANGOPYPI_ALLOW_VERSION_OVERWRITE = False

""" The upload_to argument for the file field in releases. This can either be 
a string for a path relative to your media folder or a callable. For more 
information, see http://docs.djangoproject.com/ """
if not hasattr(settings,'DJANGOPYPI_RELEASE_UPLOAD_TO'):
    settings.DJANGOPYPI_RELEASE_UPLOAD_TO = 'dists'

if not hasattr(settings,'DJANGOPYPI_OS_NAMES'):
    settings.DJANGOPYPI_OS_NAMES = (
        ("aix", "AIX"),
        ("beos", "BeOS"),
        ("debian", "Debian Linux"),
        ("dos", "DOS"),
        ("freebsd", "FreeBSD"),
        ("hpux", "HP/UX"),
        ("mac", "Mac System x."),
        ("macos", "MacOS X"),
        ("mandrake", "Mandrake Linux"),
        ("netbsd", "NetBSD"),
        ("openbsd", "OpenBSD"),
        ("qnx", "QNX"),
        ("redhat", "RedHat Linux"),
        ("solaris", "SUN Solaris"),
        ("suse", "SuSE Linux"),
        ("yellowdog", "Yellow Dog Linux"),
    )

if not hasattr(settings,'DJANGOPYPI_ARCHITECTURES'):
    settings.DJANGOPYPI_ARCHITECTURES = (
        ("alpha", "Alpha"),
        ("hppa", "HPPA"),
        ("ix86", "Intel"),
        ("powerpc", "PowerPC"),
        ("sparc", "Sparc"),
        ("ultrasparc", "UltraSparc"),
    )

if not hasattr(settings,'DJANGOPYPI_DIST_FILE_TYPES'):
    settings.DJANGOPYPI_DIST_FILE_TYPES = (
        ('sdist','Source'),
        ('bdist_dumb','"dumb" binary'),
        ('bdist_rpm','RPM'),
        ('bdist_wininst','MS Windows installer'),
        ('bdist_egg','Python Egg'),
        ('bdist_dmg','OS X Disk Image'),
    )

if not hasattr(settings,'DJANGOPYPI_PYTHON_VERSIONS'):
    settings.DJANGOPYPI_PYTHON_VERSIONS = (
        ('any','Any i.e. pure python'),
        ('2.1','2.1'),
        ('2.2','2.2'),
        ('2.3','2.3'),
        ('2.4','2.4'),
        ('2.5','2.5'),
        ('2.6','2.6'),
        ('2.7','2.7'),
        ('3.0','3.0'),
        ('3.1','3.1'),
        ('3.2','3.2'),
    )

""" These settings enable proxying of packages that are not in the local index 
to another index, http://pypi.python.org/ by default. This feature is disabled 
by default and can be enabled by setting DJANGOPYPI_PROXY_MISSING to True in 
your settings file. """
if not hasattr(settings, 'DJANGOPYPI_PROXY_BASE_URL'):
    settings.DJANGOPYPI_PROXY_BASE_URL = 'http://pypi.python.org'

if not hasattr(settings, 'DJANGOPYPI_PROXY_MISSING'):
    settings.DJANGOPYPI_PROXY_MISSING = False
