CREATE OR REPLACE PROCEDURE PROCEDUREP()
    RETURNS STRING
    LANGUAGE SQL
    EXECUTE AS OWNER
AS
$$
    BEGIN
        BEGIN TRANSACTION;
            RETURN ('Executed procedure V2!');
        COMMIT;

    EXCEPTION
        WHEN EXPRESSION_ERROR THEN
            ROLLBACK;
            RAISE;
        WHEN STATEMENT_ERROR THEN
            ROLLBACK;
            RAISE;
        WHEN OTHER THEN
            ROLLBACK;
            RAISE;
    END;
$$;
