# Tolong jangan di tambah atau kurangi file config ini karna dapat menyebabkan kesalahan configurasi saat scanning sedang berlangsung.
import re
# ==============================================================================
# SENSITIVE PATHS (Reconnaissance)
# Lebih lengkap untuk menemukan file konfigurasi, backup, dan direktori admin.
# ==============================================================================
SENSITIVE_PATHS = [
    # Source Code / Version Control
    "/.git/config", "/.svn/entries", "/.hg/hgrc", "/.bzr/branch/branch.conf",
    
    # Configuration / Environment Files
    "/.env", "/.env.local", "/config.php", "/web.config", 
    "/app/config/parameters.yml", "/settings.py", "/database.yml", 
    "/wp-config.php.bak", "/configuration.php",
    
    # Backup / Archives
    "/backup.zip", "/site.tar.gz", "/old.zip", "/archive.zip", "/site.bak", 
    "/index.php.bak", "/admin.zip",
    
    # Admin / Management Panels (Common)
    "/admin/", "/manager/", "/cpanel/", "/phpmyadmin/", "/owa/", "/jmx-console/", 
    "/server-status", "/tomcat/", "/web-inf/web.xml", "/_profiler/",
    
    # Information Disclosure
    "/robots.txt", "/sitemap.xml", "/crossdomain.xml", "/phpinfo.php", 
    "/test.php", "/info.php", "/server-info",
    
    # Hidden Files
    "/.htaccess", "/.htpasswd", "/.DS_Store",
]

# ==============================================================================
# ERROR PAGES TO TEST (Information Disclosure via Error)
# Memanfaatkan parameter umum atau path yang tidak mungkin ada.
# ==============================================================================
ERROR_PAGES_TO_TEST = {
    # 404 Testing
    404: "/non_existent_page_mak_limah_404_v2.html", 
    
    # Internal Server Error (500) Testing - common ways to trigger 500
    500: "/trigger_500_server_error",
    
    # 403 Forbidden Testing (Check if custom page is used)
    403: "/admin/nonexistent",
    
    # 400 Bad Request (Triggered by malformed request, often on parameters)
    400: "/index.php?id=%27", # Basic attempt to inject single quote to trigger error
}

# ==============================================================================
# SENSITIVE ERROR PATTERNS
# Pola yang menunjukkan adanya kebocoran informasi seperti Stack Trace, 
# path absolut file, atau informasi database.
# ==============================================================================
SENSITIVE_ERROR_PATTERNS = [
    # Stack Trace Keywords
    "stack trace", "at org.", "at java.", "on line", "in file",
    "at com.", "fatal error", "exception in thread", "typeerror", "referenceerror",
    
    # Path Disclosure
    "path is", "file:", "/var/www/", "/home/", "c:\\\\inetpub",
    
    # Database Information
    "sqlstate", "mysql_connect", "pg_connect", "oci_connect",
    "driver error", "query error", "database connection failed",
    
    # Framework Specific (e.g., PHP, Python, Java)
    "django.urls", "flask", "struts", "spring boot", "symfony",
    "a PHP Error was encountered", 
    
    # Server/Language Version Disclosure
    "apache/2.", "nginx/1.", "php version", "python 3.",
    
    # General Debug Keywords
    "debug mode", "show variables", "select * from"
]

# --- Konfigurasi Lain (Diimpor oleh mak-limah.py) ---
RECOMMENDATIONS = {
    "strict-transport-security": "Set HSTS (e.g. max-age=63072000; includeSubDomains; preload).",
    "content-security-policy": "Add Content-Security-Policy (CSP) to mitigate XSS.",
    "x-frame-options": "Set X-Frame-Options (DENY or SAMEORIGIN) to mitigate Clickjacking.",
    "x-content-type-options": "Set X-Content-Type-Options: nosniff to prevent MIME type sniffing.",
    "referrer-policy": "Consider a Referrer-Policy to control information leakage.",
    "permissions-policy": "Add Permissions-Policy to limit powerful browser features.",
    "expect-ct": "Consider Expect-CT if relevant for Certificate Transparency."
}
CRITICAL_HEADERS = ["strict-transport-security", "x-content-type-options", "content-security-policy"]

COMMON_TECH_PATTERNS = {
    "Wordpress": {"header": ["x-powered-by: PHP", "link: <*/wp-content/*>"], "text": ["wp-content", "wp-includes"]},
    "Nginx": {"header": ["server: nginx"], "text": []},
    "ASP.NET": {"header": ["x-aspnet-version", "x-powered-by: ASP.NET"], "text": []},
    "React": {"header": [], "text": ["id=\"root\"", "data-reactroot"]},
}

OPEN_REDIRECT_TEST_PARAMS = ["redirect_to", "next", "continue", "url", "target", "ret", "return", "dest", "destination", "goto", "view"]
