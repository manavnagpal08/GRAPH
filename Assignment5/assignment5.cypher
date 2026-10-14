// ==============================================================================
// ALLIANCE UNIVERSITY
// Alliance School of Advanced Computing
// Graph Analytics - Assignment 5: University Course Registration System Using Neo4j
// Student Name: Manav Nagpal | Registration Number: 2411021060402
// ==============================================================================

// ------------------------------------------------------------------------------
// 0. RESET DATABASE & CONSTRAINTS (Idempotency & Data Integrity)
// ------------------------------------------------------------------------------

// Clear any existing graph data
MATCH (n) DETACH DELETE n;

// Create Unique Constraints to avoid duplicate nodes on re-run
CREATE CONSTRAINT unique_student_id IF NOT EXISTS FOR (s:Student) REQUIRE s.studentId IS UNIQUE;
CREATE CONSTRAINT unique_faculty_id IF NOT EXISTS FOR (f:Faculty) REQUIRE f.facultyId IS UNIQUE;
CREATE CONSTRAINT unique_course_code IF NOT EXISTS FOR (c:Course) REQUIRE c.courseCode IS UNIQUE;
CREATE CONSTRAINT unique_dept_id IF NOT EXISTS FOR (d:Department) REQUIRE d.deptId IS UNIQUE;


// ==============================================================================
// PART A — GRAPH CREATION AND VERIFICATION
// ==============================================================================

// ------------------------------------------------------------------------------
// Task 1: Create all student, faculty, course, and department nodes with properties
// ------------------------------------------------------------------------------

// Create Student Nodes
MERGE (s1:Student {studentId: 'S101'})
  ON CREATE SET s1.name = 'Aarav Sharma', s1.semester = 5, s1.email = 'aarav@univ.edu';
MERGE (s2:Student {studentId: 'S102'})
  ON CREATE SET s2.name = 'Priya Das', s2.semester = 5, s2.email = 'priya@univ.edu';
MERGE (s3:Student {studentId: 'S103'})
  ON CREATE SET s3.name = 'Rahul Verma', s3.semester = 3, s3.email = 'rahul@univ.edu';
MERGE (s4:Student {studentId: 'S104'})
  ON CREATE SET s4.name = 'Sneha Roy', s4.semester = 3, s4.email = 'sneha@univ.edu';
MERGE (s5:Student {studentId: 'S105'})
  ON CREATE SET s5.name = 'Arjun Patel', s5.semester = 5, s5.email = 'arjun@univ.edu';

// Create Faculty Nodes
MERGE (f1:Faculty {facultyId: 'F101'})
  ON CREATE SET f1.name = 'Dr. Meera Sen', f1.designation = 'Associate Professor', f1.specialization = 'Database Systems';
MERGE (f2:Faculty {facultyId: 'F102'})
  ON CREATE SET f2.name = 'Dr. Amit Roy', f2.designation = 'Assistant Professor', f2.specialization = 'Data Analytics';

// Create Course Nodes
MERGE (c1:Course {courseCode: 'CS301'})
  ON CREATE SET c1.courseTitle = 'Graph Analytics', c1.credits = 3, c1.level = 'Advanced';
MERGE (c2:Course {courseCode: 'CS302'})
  ON CREATE SET c2.courseTitle = 'Database Management Systems', c2.credits = 4, c2.level = 'Core';
MERGE (c3:Course {courseCode: 'CS303'})
  ON CREATE SET c3.courseTitle = 'Data Mining', c3.credits = 3, c3.level = 'Advanced';
MERGE (c4:Course {courseCode: 'CS304'})
  ON CREATE SET c4.courseTitle = 'Big Data Analytics', c4.credits = 4, c4.level = 'Advanced';
MERGE (c5:Course {courseCode: 'CS305'})
  ON CREATE SET c5.courseTitle = 'NoSQL Databases', c5.credits = 3, c5.level = 'Core';

// Create Department Nodes
MERGE (d1:Department {deptId: 'D101'})
  ON CREATE SET d1.deptName = 'Computer Science', d1.building = 'Block A';
MERGE (d2:Department {deptId: 'D102'})
  ON CREATE SET d2.deptName = 'Information Technology', d2.building = 'Block B';


// ------------------------------------------------------------------------------
// Task 2 & Task 3: Create relationships with directions and assign properties
// Properties:
//   - ENROLLED_IN: semesterEnrolled, grade
//   - TEACHES: academicYear
// ------------------------------------------------------------------------------

// 2.A Student Enrolments (Student -> Course) with semesterEnrolled and grade
MATCH (s:Student {studentId: 'S101'}), (c:Course {courseCode: 'CS301'})
MERGE (s)-[r:ENROLLED_IN]->(c)
ON CREATE SET r.semesterEnrolled = 5, r.grade = 'Not Published';

MATCH (s:Student {studentId: 'S101'}), (c:Course {courseCode: 'CS302'})
MERGE (s)-[r:ENROLLED_IN]->(c)
ON CREATE SET r.semesterEnrolled = 5, r.grade = 'Not Published';

MATCH (s:Student {studentId: 'S101'}), (c:Course {courseCode: 'CS305'})
MERGE (s)-[r:ENROLLED_IN]->(c)
ON CREATE SET r.semesterEnrolled = 5, r.grade = 'Not Published';

MATCH (s:Student {studentId: 'S102'}), (c:Course {courseCode: 'CS301'})
MERGE (s)-[r:ENROLLED_IN]->(c)
ON CREATE SET r.semesterEnrolled = 5, r.grade = 'Not Published';

MATCH (s:Student {studentId: 'S102'}), (c:Course {courseCode: 'CS303'})
MERGE (s)-[r:ENROLLED_IN]->(c)
ON CREATE SET r.semesterEnrolled = 5, r.grade = 'Not Published';

MATCH (s:Student {studentId: 'S103'}), (c:Course {courseCode: 'CS302'})
MERGE (s)-[r:ENROLLED_IN]->(c)
ON CREATE SET r.semesterEnrolled = 3, r.grade = 'Not Published';

MATCH (s:Student {studentId: 'S103'}), (c:Course {courseCode: 'CS304'})
MERGE (s)-[r:ENROLLED_IN]->(c)
ON CREATE SET r.semesterEnrolled = 3, r.grade = 'Not Published';

MATCH (s:Student {studentId: 'S104'}), (c:Course {courseCode: 'CS303'})
MERGE (s)-[r:ENROLLED_IN]->(c)
ON CREATE SET r.semesterEnrolled = 3, r.grade = 'Not Published';

MATCH (s:Student {studentId: 'S104'}), (c:Course {courseCode: 'CS305'})
MERGE (s)-[r:ENROLLED_IN]->(c)
ON CREATE SET r.semesterEnrolled = 3, r.grade = 'Not Published';

MATCH (s:Student {studentId: 'S105'}), (c:Course {courseCode: 'CS301'})
MERGE (s)-[r:ENROLLED_IN]->(c)
ON CREATE SET r.semesterEnrolled = 5, r.grade = 'Not Published';

MATCH (s:Student {studentId: 'S105'}), (c:Course {courseCode: 'CS304'})
MERGE (s)-[r:ENROLLED_IN]->(c)
ON CREATE SET r.semesterEnrolled = 5, r.grade = 'Not Published';

// 2.B Faculty Teaching Assignments (Faculty -> Course) with academicYear
MATCH (f:Faculty {facultyId: 'F101'}), (c:Course {courseCode: 'CS302'})
MERGE (f)-[r:TEACHES]->(c)
ON CREATE SET r.academicYear = '2026-27';

MATCH (f:Faculty {facultyId: 'F101'}), (c:Course {courseCode: 'CS305'})
MERGE (f)-[r:TEACHES]->(c)
ON CREATE SET r.academicYear = '2026-27';

MATCH (f:Faculty {facultyId: 'F102'}), (c:Course {courseCode: 'CS301'})
MERGE (f)-[r:TEACHES]->(c)
ON CREATE SET r.academicYear = '2026-27';

MATCH (f:Faculty {facultyId: 'F102'}), (c:Course {courseCode: 'CS303'})
MERGE (f)-[r:TEACHES]->(c)
ON CREATE SET r.academicYear = '2026-27';

MATCH (f:Faculty {facultyId: 'F102'}), (c:Course {courseCode: 'CS304'})
MERGE (f)-[r:TEACHES]->(c)
ON CREATE SET r.academicYear = '2026-27';

// 2.C Student-Department Associations (Student -> Department)
MATCH (s1:Student {studentId: 'S101'}), (d1:Department {deptId: 'D101'})
MERGE (s1)-[:BELONGS_TO]->(d1);

MATCH (s2:Student {studentId: 'S102'}), (d1:Department {deptId: 'D101'})
MERGE (s2)-[:BELONGS_TO]->(d1);

MATCH (s3:Student {studentId: 'S103'}), (d1:Department {deptId: 'D101'})
MERGE (s3)-[:BELONGS_TO]->(d1);

MATCH (s4:Student {studentId: 'S104'}), (d2:Department {deptId: 'D102'})
MERGE (s4)-[:BELONGS_TO]->(d2);

MATCH (s5:Student {studentId: 'S105'}), (d2:Department {deptId: 'D102'})
MERGE (s5)-[:BELONGS_TO]->(d2);

// 2.D Department-Course Associations (Department -> Course)
MATCH (d1:Department {deptId: 'D101'}), (c2:Course {courseCode: 'CS302'})
MERGE (d1)-[:OFFERS]->(c2);

MATCH (d1:Department {deptId: 'D101'}), (c3:Course {courseCode: 'CS303'})
MERGE (d1)-[:OFFERS]->(c3);

MATCH (d1:Department {deptId: 'D101'}), (c5:Course {courseCode: 'CS305'})
MERGE (d1)-[:OFFERS]->(c5);

MATCH (d2:Department {deptId: 'D102'}), (c1:Course {courseCode: 'CS301'})
MERGE (d2)-[:OFFERS]->(c1);

MATCH (d2:Department {deptId: 'D102'}), (c4:Course {courseCode: 'CS304'})
MERGE (d2)-[:OFFERS]->(c4);


// ------------------------------------------------------------------------------
// Task 4: Display the complete graph
// ------------------------------------------------------------------------------
MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m;


// ------------------------------------------------------------------------------
// Task 5: Count the number of nodes belonging to each label
// ------------------------------------------------------------------------------
MATCH (n)
RETURN labels(n)[0] AS Label, count(n) AS NodeCount
ORDER BY Label;


// ------------------------------------------------------------------------------
// Task 6: Display all relationship types and verify their directions
// ------------------------------------------------------------------------------
MATCH (a)-[r]->(b)
RETURN labels(a)[0] AS SourceNode, type(r) AS RelationshipType, labels(b)[0] AS TargetNode, count(r) AS Count
ORDER BY RelationshipType, SourceNode;


// ==============================================================================
// PART B — RETRIEVAL AND FILTERING QUERIES
// ==============================================================================

// ------------------------------------------------------------------------------
// Task 7: Retrieve all students studying in Semester 5
// ------------------------------------------------------------------------------
MATCH (s:Student)
WHERE s.semester = 5
RETURN s.studentId AS StudentID, s.name AS Name, s.semester AS Semester, s.email AS Email
ORDER BY s.studentId;


// ------------------------------------------------------------------------------
// Task 8: Find all courses with more than 3 credits
// ------------------------------------------------------------------------------
MATCH (c:Course)
WHERE c.credits > 3
RETURN c.courseCode AS CourseCode, c.courseTitle AS CourseTitle, c.credits AS Credits, c.level AS Level
ORDER BY c.courseCode;


// ------------------------------------------------------------------------------
// Task 9: Retrieve the courses taught by Dr. Meera Sen
// ------------------------------------------------------------------------------
MATCH (f:Faculty {name: 'Dr. Meera Sen'})-[r:TEACHES]->(c:Course)
RETURN f.name AS FacultyName, c.courseCode AS CourseCode, c.courseTitle AS CourseTitle, c.credits AS Credits, r.academicYear AS AcademicYear
ORDER BY c.courseCode;


// ------------------------------------------------------------------------------
// Task 10: Find all students enrolled in Graph Analytics
// ------------------------------------------------------------------------------
MATCH (s:Student)-[r:ENROLLED_IN]->(c:Course)
WHERE c.courseTitle = 'Graph Analytics'
RETURN s.studentId AS StudentID, s.name AS StudentName, s.semester AS CurrentSemester, c.courseTitle AS EnrolledCourse
ORDER BY s.studentId;


// ------------------------------------------------------------------------------
// Task 11: Display the names of all students belonging to the Computer Science department
// ------------------------------------------------------------------------------
MATCH (s:Student)-[:BELONGS_TO]->(d:Department)
WHERE d.deptName = 'Computer Science'
RETURN s.studentId AS StudentID, s.name AS StudentName, d.deptName AS DepartmentName, d.building AS Building
ORDER BY s.studentId;


// ------------------------------------------------------------------------------
// Task 12: Find all courses offered by the Information Technology department
// ------------------------------------------------------------------------------
MATCH (d:Department)-[:OFFERS]->(c:Course)
WHERE d.deptName = 'Information Technology'
RETURN d.deptName AS DepartmentName, c.courseCode AS CourseCode, c.courseTitle AS CourseTitle, c.credits AS Credits, c.level AS Level
ORDER BY c.courseCode;


// ------------------------------------------------------------------------------
// Task 13: Retrieve all students enrolled in NoSQL Databases along with their semester and grade
// ------------------------------------------------------------------------------
MATCH (s:Student)-[r:ENROLLED_IN]->(c:Course)
WHERE c.courseTitle = 'NoSQL Databases'
RETURN s.studentId AS StudentID, s.name AS StudentName, s.semester AS StudentSemester, r.semesterEnrolled AS SemesterEnrolled, r.grade AS Grade, c.courseTitle AS CourseTitle
ORDER BY s.studentId;


// ------------------------------------------------------------------------------
// Task 14: Find all students enrolled in both Graph Analytics and another course
// ------------------------------------------------------------------------------
// Form A: Pairwise detail
MATCH (s:Student)-[:ENROLLED_IN]->(c1:Course {courseTitle: 'Graph Analytics'}),
      (s:Student)-[:ENROLLED_IN]->(c2:Course)
WHERE c1 <> c2
RETURN s.studentId AS StudentID, s.name AS StudentName, c1.courseTitle AS PrimaryCourse, c2.courseTitle AS OtherCourse
ORDER BY s.studentId, c2.courseTitle;

// Form B: Aggregated list of other courses per student
MATCH (s:Student)-[:ENROLLED_IN]->(c1:Course {courseTitle: 'Graph Analytics'}),
      (s:Student)-[:ENROLLED_IN]->(c2:Course)
WHERE c1 <> c2
RETURN s.studentId AS StudentID, s.name AS StudentName, collect(c2.courseTitle) AS OtherCoursesEnrolled
ORDER BY s.studentId;
