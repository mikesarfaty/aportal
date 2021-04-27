-- depends: 00.init

USE hzportal;

/* not sure why I made 00.init, but at this point it's a step 0 for the migrations so it can chill */
CREATE TABLE users (
    user_id INT AUTO_INCREMENT,
    full_name VARCHAR(255) NOT NULL,
    graduating_year INT NOT NULL,
    graduating_semester ENUM('SPR', 'S1', 'S2', 'FALL'),
    major VARCHAR(255) NOT NULL,
    pw_hash VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    notes VARCHAR(255),  -- idk maybe you wanna flex on the h8rs and put something edgy here
    UNIQUE(username),
    PRIMARY KEY (user_id)
);

/*
    basic permissions
    ==
    Using a table instead of an ENUM for user roles so that I can refer back to it in
    role_assignments as well as add more when needed
 */
CREATE TABLE user_roles (
    role_name VARCHAR(255) NOT NULL,
    UNIQUE(role_name)
);

INSERT INTO
    user_roles (role_name)
VALUES
    ('USER'),
    ('ADMIN'),
    ('SUPER'),
    ('EXEC');

CREATE TABLE role_assignments (
    user_id INT PRIMARY KEY NOT NULL,
    role_name VARCHAR(255) NOT NULL,
    UNIQUE(user_id, role_name),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (role_name) REFERENCES user_roles(role_name) ON UPDATE CASCADE ON DELETE CASCADE
);