-- depends: 01.users
USE hzportal;

CREATE TABLE courses (
    course_id INT AUTO_INCREMENT NOT NULL,
    course_prefix VARCHAR(255) NOT NULL,
    course_number VARCHAR(255) NOT NULL,
    course_fullname VARCHAR(255) NOT NULL,
    college VARCHAR(255),
    UNIQUE (course_prefix, course_number),
    CHECK (course_prefix RLIKE '[0-9]{4}'),
    PRIMARY KEY (course_id)
);

CREATE TABLE taken_courses (
    taken_course_id INT AUTO_INCREMENT NOT NULL,
    course_id INT NOT NULL,
    user_id INT NOT NULL,
    semester_taken ENUM('SPR', 'S1', 'S2', 'FALL') NOT NULL,
    year_taken INT NOT NULL,
    date_started DATE,
    date_completed DATE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE(course_id, user_id, semester_taken, year_taken),
    CHECK (year_taken > 2000),
    PRIMARY KEY (taken_course_id)
);

DELIMITER $$

CREATE PROCEDURE update_date_started_and_completed
(IN semester_taken_param VARCHAR(255), year_taken_param INT, taken_course_id_param INT)
BEGIN
DECLARE date_started_var DATE;
DECLARE date_completed_var DATE;

SELECT 
    CASE
        WHEN semester_taken_param = 'SPR' THEN CONCAT('01/01/', year_taken_param)
        WHEN semester_taken_param = 'S1' THEN CONCAT('05/01/', year_taken_param)
        WHEN semester_taken_param = 'S2' THEN CONCAT('07/01/', year_taken_param)
        WHEN semester_taken_param = 'FALL' THEN CONCAT('09/01/', year_taken_param)
    END,
    CASE
        WHEN semester_taken_param = 'SPR' THEN CONCAT('04/25/', year_taken_param)
        WHEN semester_taken_param = 'S1' THEN CONCAT('06/25/', year_taken_param)
        WHEN semester_taken_param = 'S2' THEN CONCAT('08/25/', year_taken_param)
        WHEN semester_taken_param = 'FALL' THEN CONCAT('12/25/', year_taken_param)
    END
    INTO date_started_var, date_completed_var;

    UPDATE taken_courses
    SET date_started=date_started_var, date_completed=date_completed_var
    WHERE taken_course_id = taken_course_id_param;
END $$

CREATE TRIGGER set_taken_courses_start_and_end_dates_trigger
AFTER INSERT ON taken_courses
FOR EACH ROW
BEGIN
	CALL update_date_started_and_completed(NEW.semester_taken, NEW.year_taken, NEW.taken_course_id);
END $$

DELIMITER ;
