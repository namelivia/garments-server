--Insert garment types 
INSERT INTO garment_types (id, name) VALUES (1, 'Test Garment Type 1');
INSERT INTO garment_types (id, name) VALUES (2, 'Test Garment Type 2');

--Insert places 
INSERT INTO places (id, name) VALUES (1, 'Test Place 1');
INSERT INTO places (id, name) VALUES (2, 'Test Place 2');

--Insert activities
INSERT INTO activities (id, name) VALUES (1, 'Test Activity 1');
INSERT INTO activities (id, name) VALUES (2, 'Test Activity 2');

--Insert test user data
INSERT INTO user_data (id, user_id, place) VALUES (1, 'localhost/testuser', 'Test Place 1');
INSERT INTO user_data (id, user_id, place) VALUES (2, 'localhost/testuser2', 'Test Place 2');

--Insert some test garments
INSERT INTO garments (id, name, garment_type, color, status, journaling_key, image, place, activity) VALUES (1, 'Test garment 1', 'Test Garment Type 1', 'Test color 1', 'Test status 1', gen_random_uuid(), 'some_image_url', 'Test Place 1', 'Test Activity 1');
INSERT INTO garments (id, name, garment_type, color, status, journaling_key, image, place, activity) VALUES (2, 'Test garment 2', 'Test Garment Type 2', 'Test color 2', 'Test status 2', gen_random_uuid(), 'some_image_url_2', 'Test Place 1', 'Test Activity 1');
INSERT INTO garments (id, name, garment_type, color, status, journaling_key, image, place, activity) VALUES (3, 'Test garment 3', 'Test Garment Type 1', 'Test color 1', 'Test status 1', gen_random_uuid(), 'some_image_url_3', 'Test Place 1', 'Test Activity 1');
INSERT INTO garments (id, name, garment_type, color, status, journaling_key, image, place, activity) VALUES (4, 'Test garment 4', 'Test Garment Type 2', 'Test color 2', 'Test status 2', gen_random_uuid(), 'some_image_url_4', 'Test Place 2', 'Test Activity 1');
INSERT INTO garments (id, name, garment_type, color, status, journaling_key, image, place, activity) VALUES (5, 'Test garment 5', 'Test Garment Type 1', 'Test color 1', 'Test status 1', gen_random_uuid(), 'some_image_url', 'Test Place 1', 'Test Activity 2');
INSERT INTO garments (id, name, garment_type, color, status, journaling_key, image, place, activity) VALUES (6, 'Test garment 6', 'Test Garment Type 2', 'Test color 2', 'Test status 2', gen_random_uuid(), 'some_image_url_2', 'Test Place 1', 'Test Activity 2');
INSERT INTO garments (id, name, garment_type, color, status, journaling_key, image, place, activity) VALUES (7, 'Test garment 7', 'Test Garment Type 1', 'Test color 1', 'Test status 1', gen_random_uuid(), 'some_image_url_3', 'Test Place 1', 'Test Activity 2');
INSERT INTO garments (id, name, garment_type, color, status, journaling_key, image, place, activity) VALUES (8, 'Test garment 8', 'Test Garment Type 2', 'Test color 2', 'Test status 2', gen_random_uuid(), 'some_image_url_4', 'Test Place 2', 'Test Activity 2');
