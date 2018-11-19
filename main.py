#!/usr/bin/env python3
import requests, argparse, pyquery

logs = False

def lprint(*message):
    if(logs):
        print('  '.join(str(i) for i in message))

def parse_courses (courseIds, links):
    coursesLinks = []
    for courseId in courseIds:
        lprint("Fetching %s started." % courseId)
        if not check_course_id(courseId):
            return false
        coursesLinks.append(parse_course(courseId, links))
        lprint("Fetching %s finished." % courseId)
    return coursesLinks

def parse_course(courseId, links):
    courseLinks = []
    i = 1
    while True:
        lprint("Trying for lesson", i)
        res = requests.get("http://maktabkhooneh.org/course/%s/lesson/%s/" % (courseId, i))
        if "lesson" not in res.url:
            break
        if res.status_code != 200:
            break
        i += 1

        pq = pyquery.PyQuery(res.text)
        downloadLink = pq("meta[property='og:video']").attr('content')

        courseLinks.append(downloadLink)
        if links:
            continue
        download_link(downloadLink, courseId, i-1)
        if downloadLink != None:
            lprint("%s" % downloadLink)
        else:
            break
        #print("%s" % downloadLink)
    return courseLinks


def check_course_id (courseId):
    """
    to be implemented.
    """
    return True

def download_link (downloadLink, courseId, lessonId):
    url = downloadLink
    r = requests.get(url, allow_redirects=True)

    open('./{}-{}.mp4'.format(courseId, lessonId), 'wb').write(r.content)
    return True

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Download helper for maktabkhooneh courses.')
    parser.add_argument('courseIds', metavar='course_id', nargs='+', help='Insert course(s) id')
    parser.add_argument('--links', action='store_const', const=True, default=False, help='Return links to std output')
    parser.add_argument('--logs', action='store_const', const=True, default=False, help='Verbose mode for debug')
    args = parser.parse_args()

    logs = args.logs

    coursesLinks = parse_courses(args.courseIds, args.links)
    if args.links:
        for courseLinks in coursesLinks:
            print("\n".join(courseLinks))
        print("\n")
