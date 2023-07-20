CREATE OR REPLACE FUNCTION check_same_sensor() 
RETURNS TRIGGER AS 
$$
BEGIN 
    IF (NEW.sensor != OLD.sensor) THEN
        RAISE EXCEPTION 'Sensor ID cannot be changed';
    END IF;

    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS check_same_sensor ON sensor_values;
CREATE CONSTRAINT TRIGGER check_same_sensor 
BEFORE INSERT OR UPDATE ON sensor_values DEEFERRABLE
FOR EACH ROW EXECUTE FUNCTION check_same_sensor();