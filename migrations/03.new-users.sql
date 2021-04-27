-- depends: 01.users

/*
This file is a cheat-code for signing up. There's probably a better way to do this
re-using the users table, but I like to think of users as having two-steps (registered and un-registered)
*/

CREATE TABLE unregistered_users (
    username VARCHAR(64) NOT NULL,
    full_name VARCHAR(64) NOT NULL,
    user_id INT, -- updated once user is created
    registration_hash VARCHAR(128) NOT NULL, -- treat this as PK so that user reg doesn't show user_id ??
    PRIMARY KEY (registration_hash),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
    UNIQUE(username)
);

DELIMITER //
CREATE PROCEDURE register_user
(IN registration_hash_param VARCHAR(128),
graduating_year_param INT,
graduating_semester_param ENUM('SPR', 'S1', 'S2', 'FALL'),
major_param VARCHAR(255),
pw_hash_param VARCHAR(255)
)
BEGIN
    DECLARE full_name_var VARCHAR(64);
    DECLARE username_var VARCHAR(64);
    DECLARE cur_user_id_var INT;
    DECLARE new_user_id_var INT;

    SELECT full_name, username, user_id
    INTO full_name_var, username_var, cur_user_id_var
    FROM unregistered_users
    WHERE registration_hash=registration_hash_param;

    START TRANSACTION; -- user IDs can change concurrently so group this Txn
    IF NOT ISNULL(cur_user_id_var) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT 'user already registered'
    END IF;
    SELECT MAX(user_id) + 1
    INTO new_user_id_var
    FROM users;

    INSERT INTO
        users(
            user_id,
            full_name,
            graduating_year,
            graduating_semester,
            major,
            pw_hash,
            username
        )
    VALUES
        (
            new_user_id_var,
            full_name_var,
            graduating_year_param,
            graduating_semester_param,
            major_param,
            pw_hash_param,
            username_var
        );

    UPDATE unregistered_users
    SET user_id=new_user_id_var
    WHERE registration_hash=registration_hash_param;
    COMMIT; -- end of Txn which uses user_ids
END //

DELIMITER ;