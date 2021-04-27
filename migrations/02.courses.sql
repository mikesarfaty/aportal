-- depends: 01.users
USE hzportal;

CREATE TABLE IF NOT EXISTS courses (
    course_id INT AUTO_INCREMENT NOT NULL,
    course_prefix VARCHAR(255) NOT NULL,
    course_number VARCHAR(255) NOT NULL,
    course_fullname VARCHAR(255) NOT NULL,
    college VARCHAR(255),
    UNIQUE (course_prefix, course_number),
    CHECK (course_number RLIKE '[0-9]{4}'),
    CHECK (course_prefix RLIKE '[A-Z]{2,3}'),
    PRIMARY KEY (course_id)
);

CREATE TABLE IF NOT EXISTS taken_courses (
    taken_course_id INT AUTO_INCREMENT NOT NULL,
    course_id INT NOT NULL,
    user_id INT NOT NULL,
    semester_taken ENUM('SPR', 'S1', 'S2', 'FALL') NOT NULL,
    year_taken INT NOT NULL,
    date_started DATE,
    date_completed DATE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
    UNIQUE(course_id, user_id, semester_taken, year_taken),
    CHECK (year_taken > 2000),
    PRIMARY KEY (taken_course_id)
);

DELIMITER $$

CREATE PROCEDURE update_date_started_and_completed
(
    IN semester_taken_param VARCHAR(255), 
    IN year_taken_param INT,
    IN taken_course_id_param INT,
    OUT date_started_out DATE,
    OUT date_ended_out DATE
)
BEGIN
DECLARE date_started_var DATE;
DECLARE date_completed_var DATE;

SELECT 
    CASE
        WHEN semester_taken_param = 'SPR' THEN CONCAT(year_taken_param, '-01-01')
        WHEN semester_taken_param = 'S1' THEN CONCAT(year_taken_param, '-05-01')
        WHEN semester_taken_param = 'S2' THEN CONCAT(year_taken_param, '-07-01')
        WHEN semester_taken_param = 'FALL' THEN CONCAT(year_taken_param, '-09-01')
    END,
    CASE
        WHEN semester_taken_param = 'SPR' THEN CONCAT(year_taken_param, '-04-25')
        WHEN semester_taken_param = 'S1' THEN CONCAT(year_taken_param, '-06-25')
        WHEN semester_taken_param = 'S2' THEN CONCAT(year_taken_param, '-08-25')
        WHEN semester_taken_param = 'FALL' THEN CONCAT(year_taken_param, '-12-25')
    END
    INTO date_started_var, date_completed_var;

    SELECT date_started_var, date_completed_var
    INTO @date_started_out, @date_ended_out;
END $$

CREATE TRIGGER set_taken_courses_start_and_end_dates_trigger
BEFORE INSERT ON taken_courses
FOR EACH ROW
BEGIN
    DECLARE date_started_var DATE;
    DECLARE date_completed_var DATE;

    CALL update_date_started_and_completed(
        NEW.semester_taken,
        NEW.year_taken,
        NEW.taken_course_id,
        @date_started_out,
        @date_ended_out);

    SET NEW.date_started=@date_started_out;
    SET NEW.date_completed=@date_ended_out;
END $$

DELIMITER ;
