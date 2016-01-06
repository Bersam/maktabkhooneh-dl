#!/usr/bin/env python3
import requests, argparse, pyquery

def parse_courses (courseIds, links):
    coursesLinks = []
    for courseId in courseIds:
        print("Fetching %s started." % courseId)
        if not check_course_id(courseId):
            return false
        coursesLinks.append(parse_course(courseId, links))
        print("Fetching %s finished." % courseId)
    return coursesLinks

def parse_course(courseId, links):
    courseLinks = []
    i = 1
    while True:
        res = requests.get("http://maktabkhooneh.org/video/%s-%d" % (courseId, i))
        if res.status_code != 200:
            break
        i += 1

        pq = pyquery.PyQuery(res.text)
        downloadLink = pq("a.hq-video-dl").attr('href')

        courseLinks.append(downloadLink)
        if links:
            continue
        download_link(downloadLink)
        print("download link %s" % downloadLink)
    return courseLinks


def check_course_id (courseId):
    """
    to be implemented.
    """
    return True

def download_link (downloadLink):
    """
    to be implemented.
    """
    return True

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Download helper for maktabkhooneh courses.')
    parser.add_argument('courseIds', metavar='course_id', nargs='+', help='Insert course(s) id')
    parser.add_argument('--links', action='store_const', const=True, default=False, help='Return links to std output')
    args = parser.parse_args()

    coursesLinks = parse_courses(args.courseIds, args.links)
    if args.links:
        for courseLinks in coursesLinks:
            print("\n".join(courseLinks))
        print("\n")

