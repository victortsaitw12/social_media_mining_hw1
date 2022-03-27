#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from hahow import Hahow
import pandas as pd

def prepareCourseFrame(data):
    result = []
    columns = ['_id', 'title', 'numRating', 'averageRating', 'totalVideoLengthInSeconds',
               'createdAt', 'numSoldTickets', 'price', 'preOrderedPrice', 'publishTime']
    for t in data:
        d = { key: t[key] if key in t.keys() else 0 for key in columns}
        d['groupId'] = ''
        d['groupTitle'] = ''
        d['groupName'] = ''
        d['subGroupId'] = ''
        d['subGroupTitle'] = ''
        d['subGroupName'] = ''
        if('group' in t.keys()):
            d['groupId'] = t['group']['_id']
            d['groupTitle'] = t['group']['title']
            d['groupName'] = t['group']['uniquename']
            d['subGroupId'] = t['group']['subGroup']['_id']
            d['subGroupTitle'] = t['group']['subGroup']['title']
            d['subGroupName'] = t['group']['subGroup']['uniquename']
        result.append(d)
    df = pd.DataFrame(result)
    df.set_index("_id", inplace=True)
    return df

def saveCoursesToCSV(h):
    df_course_1 = prepareCourseFrame(h.getAllTopCourseInDB())
    df_course_2 = prepareCourseFrame(h.getAllCoursesInDB())
    df = pd.concat([df_course_1, df_course_2])
    df = df[~df.index.duplicated(keep='last')]
    df.to_csv("course.csv")

def saveStudentsToCSV(h):
    columns = ['_id', 'name', 'numBookmarkedCourse', 'numBookmarkedIdea', 'numBoughtCourse',
               'numCreation', 'numIdea', 'numTaughtCourse']
    df = pd.DataFrame()
    for t in h.getAllStudentsInDB():
        d = { key: t[key] if key in t.keys() else 0 for key in columns}
        df = pd.concat([df, pd.DataFrame([d])])
    df.set_index("_id", inplace=True)
    df.to_csv("student.csv")

def  prepareLinkDataFrame(t, type):
    data = []
    for courseId in t[type]:
        data.append({
          'student': t['_id'],
          'course': courseId,
          'type': type
        })
    return pd.DataFrame(data)

def saveLinksToCSV(h):
    df = pd.DataFrame()
    for t in h.getAllStudentsInDB():
        df_bought = prepareLinkDataFrame(t, 'boughtCourses')
        df_bookmarked = prepareLinkDataFrame(t, 'bookmarkedCourses')
        df_tought = prepareLinkDataFrame(t, 'toughtCourses')
        df = pd.concat([df, df_bought, df_bookmarked, df_tought])
    df.set_index(["student", "course"], inplace=True)
    df.to_csv("link.csv")

def saveTopCourses(h):

    # Collect Courses having most students
    courses = h.collectCouses()

    # Save top courses
    for courseId in courses:

        # check if data is existed in db
        old = h.getTopCourseInDB(courseId)
        if(old):
            continue

        courseInfo = h.getCourseDetail(courseId)
        studentIds = h.getStudentIds(courseId)
        courseInfo['students'] = studentIds

        h.saveTopCourse(courseInfo)


def saveStudents(h):

    studentIds = h.getStudentIdsForAllCourses()

    for studentId in studentIds:

        # check if data is existed in db
        old = h.getStudentInDB(studentId)
        if(old):
            continue

        student = h.getUserDetail(studentId)

        if(student['numBoughtCourse'] == 0):
            student['boughtCourses'] = []
        else:
            student['boughtCourses'] = h.getUserBoughtCourse(studentId)

        if(student['numBookmarkedCourse'] == 0):
            student['bookmarkedCourses'] = []
        else:
            student['bookmarkedCourses'] = h.getUserbookmarkedCourse(studentId)

        if(student['numTaughtCourse'] == 0):
            student['toughtCourses'] = []
        else:
            student['toughtCourses'] = h.getUserToughtCourse(studentId)

        h.saveStudent(student)


def saveCourses(h):

    courses = h.getCourseIdsForAllStudents()

    for courseId in allCourses:        

        # check if data is existed in db
        old = h.getCourseInDB(courseId)
        if(old):
            continue

        courseInfo = h.getCourseDetail(courseId)
        h.saveCourse(courseInfo)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--save', type=str, help = "Please Input Command")
    parser.add_argument('-t', '--transform', type=str, help = "Please Input file name")
    parser.add_argument('--db', type=str, help = "Please Input MongoDB Connection")
    args = parser.parse_args()

    if(not args.db):
        raise 'Please Input MongoDB Connection'

    if(not args.save and not args.transform):
        raise 'Please Input actions'

    h = Hahow(args.db)

    if(args.save == 'student'):
        saveStudents(h)

    if(args.save == 'top'):
        saveTopCourses(h)

    if(args.save == 'course'):
        saveCourses(h)     

    if(args.transform == 'course'):
        saveCoursesToCSV(h)

    if(args.transform == 'student'):
        saveStudentsToCSV(h)

    if(args.transform == 'link'):
        saveLinksToCSV(h)

    if(args.transform == 'test'):
        h.test()
