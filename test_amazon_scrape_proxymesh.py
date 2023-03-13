import shlex
import subprocess
import requests


"""
Test proxymesh via Python requests library vs. cURL.
"""


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17'
AMAZON_URL = 'https://www.amazon.com/dp/B0BWLRQRMZ'
PROXY_HOST = 'us-ca.proxymesh.com'
PROXY_PORT = 31280
PROXY_USER = ''
PROXY_PASS = ''


def get_response_via_requests():
    """
    Uses requests lib without sessions and simpler proxy config.
    """
    proxies = {'https': 'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'.format(
        proxy_user=PROXY_USER,
        proxy_pass=PROXY_PASS,
        proxy_host=PROXY_HOST,
        proxy_port=PROXY_PORT
    )}
    response = requests.get(AMAZON_URL,
                            proxies=proxies,
                            headers={
                                'authority': 'www.amazon.com',
                                'User-Agent': USER_AGENT
                            })
    return response.content


def get_response_via_curl():
    """
    Uses cURL.
    """
    cmd = """
      curl 
      --compressed 
      -x http://{proxy_host}:{proxy_port} 
      -U {proxy_user}:{proxy_pass} 
      --header "authority: www.amazon.com" 
      --header "User-Agent: {user_agent}" 
      -i {url} 
    """.format(
        proxy_user=PROXY_USER,
        proxy_pass=PROXY_PASS,
        proxy_host=PROXY_HOST,
        proxy_port=PROXY_PORT,
        user_agent=USER_AGENT,
        url=AMAZON_URL
    )
    output = subprocess.check_output(shlex.split(cmd))
    return output


def parse_is_success(response_body):
    # A legitimate Amazon payload will have this tacked on to the end of the HTML
    return '.__(.)< (MEOW)' in response_body.decode()


def process_response(response):
    is_success = parse_is_success(response)
    if is_success:
        print('success')
    else:
        print('fail')


def main():
    print('using requests...')
    for _ in range(10):
        try:
            r = get_response_via_requests()
            process_response(r)
        except requests.exceptions.ProxyError:
            print('proxy error')

    print('using curl...')
    for _ in range(10):
        try:
            r = get_response_via_curl()
            process_response(r)
        except subprocess.CalledProcessError:
            print('curl error')


if __name__ == '__main__':
    main()
