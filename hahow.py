#!/usr/bin/python
# -*- coding: utf-8 -*-
from api import Api
from database import Database

class Hahow:
    def __init__(self, db):
        self._hahow = Api('https://api.hahow.in/api', 3)
        self._db = Database(db, 'social_media')

    def collectCouses(self, sizeOfCourses = 100):
        courseIds = []
        pageIndex = 0
        while len(courseIds) < sizeOfCourses:
            path = '/courses?limit=24&page=%s&sort=NUM_OF_STUDENT&status=PUBLISHED'
            resp = self._hahow.goto(path % pageIndex)
            courseIds.extend([data['_id'] for data in resp['data']])
            pageIndex = pageIndex + 1
        return courseIds

    def getStudentIds(self, courseId):
        discussions = self.collectDiscussions(courseId)
        studentIds = [comment['owner']['_id'] for comment in discussions]
        return studentIds

    def getCourseDetail(self, course):
        path = '/courses/%s?requestBackup=false'
        print("getCourseDetail:course:%s", course)
        return self._hahow.goto(path % course)

    def collectDiscussions(self, course):
        path = '/courses/' + course + '/discussions?limit=20&page=%s'       
        pageIndex  = 0
        discussions = []
        while(True):
            resp = self._hahow.goto(path % pageIndex)
            if(len(resp) == 0):
                break
            discussions.extend(resp)
            pageIndex = pageIndex + 1
        return discussions

    def getUserDetail(self, user):
        path = '/users/%s'
        return self._hahow.goto(path % user)
  
    def getUserBoughtCourse(self, user):
        path = '/users/%s/boughtCourses'
        resp = self._hahow.goto(path % user)
        if('errorCode' in resp and resp['errorCode'] == 20001):
            print(resp)
            return []
        return [data['_id'] for data in resp]

    def getUserToughtCourse(self, user):
        path = '/users/%s/taughtCourses'
        resp = self._hahow.goto(path % user)
        if('errorCode' in resp and resp['errorCode'] == 20001):
            return []
        return [data['_id'] for data in resp]

    def getUserbookmarkedCourse(self, user):
        path = '/users/%s/bookmarkedCourses'
        resp = self._hahow.goto(path % user)
        if('errorCode' in resp and resp['errorCode'] == 20001):
            return []
        return [data['_id'] for data in resp]

    def getCategories(self):
        pass

    def getStudentIdsForAllCourses(self):
        allStudents = []
        for course in self._db.findAll('top_course'):
            allStudents.extend(course['students'])
        return set(allStudents)

    def getCourseIdsForAllStudents(self):
        allCourses = []
        for student in self._db.findAll('student'):
            allCourses.extend(student['boughtCourses'])
            allCourses.extend(student['toughtCourses'])
            allCourses.extend(student['bookmarkedCourses'])
        return set(allCourses)

    def getAllTopCourseInDB(self):
        return self._db.findAll('top_course')

    def getTopCourseInDB(self, courseId):
        return self._db.findById('top_course', courseId)

    def saveTopCourse(self, data):
        return self._db.insert('top_course', data)

    def getAllStudentsInDB(self):
        return self._db.findAll('student')

    def getStudentInDB(self, id):
        return self._db.findById('student', id)

    def saveStudent(self, data):
        return self._db.insert('student', data)

    def getAllCoursesInDB(self):
        return self._db.findAll('course')

    def getCourseInDB(self, id):
        return self._db.findById('course', id)

    def saveCourse(self, data):
        return self._db.insert('course', data)

    def test(self):
        for c in self.getAllTopCourseInDB():
            print(c)
