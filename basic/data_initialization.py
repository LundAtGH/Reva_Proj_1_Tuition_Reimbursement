from basic.util.db_connection import connection


def initialize_data():
    sql = """
    drop
    table if exists
    reimbursements;
    drop
    table if exists
    employees;
    
    CREATE
    TABLE
    employees
    (
        id            bigserial PRIMARY KEY,
    supervisor_id bigserial,
    job           varchar(100),
    name
    varchar(50),
    password
    varchar(15),
    email
    varchar(255),
    phone
    varchar(20)
    );
    
    
    CREATE
    TABLE
    reimbursements
    (
        id             bigserial PRIMARY KEY,
    employee_id    bigserial REFERENCES employees(id)
    ON
    DELETE
    SET
    NULL,
    class_type
    varchar(100),
    funds
    numeric(10, 2)
    CHECK(funds >= 0),
    approval_stage
    int,
    stage_reason
    varchar(500),
    
    grade_or_presentation
    varchar(2000),
    date_of_last_escalation
    bigint,
    date_requested
    bigint,
    date_starting
    bigint
    );
    
    insert
    into
    employees
    values
    (
        default,
        -1,
        'Benefits Coordinator',
        'Kevin',
        'q',
        'none',
        '555-555-5555'
    );
    
    insert
    into
    employees
    values
    (
        default,
        -1,
        'Dept. Head',
        'John',
        'q',
        'none',
        '555-555-5555'
    );
    
    insert
    into
    employees
    values
    (
        default,
        2,
        'Supervisor',
        'Fred',
        'q',
        'none',
        '555-555-5555'
    );
    
    insert
    into
    employees
    values
    (
        default,
        3,
        'Peon',
        'Barbra',
        'q',
        'none',
        '555-555-5555'
    );
    
    
    
    
    insert
    into
    reimbursements
    values
    (
        default,
        4,
        'University Course',
        1000.00,
        3,
        '3 (Req. by Barbra):(br)Necessary for latest assignment.(br)(br)Prior approval history unknown!',
        'youtube.com/Python+Presentation', -- url to unlisted YT video?
    20210101,
    20210101,
    20210101
    );
    
    """

    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
