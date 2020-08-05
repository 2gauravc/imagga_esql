
/*Table structure for table customers */
DROP TABLE IF EXISTS image_tags CASCADE;
CREATE TABLE image_tags(
  image_name varchar(50) NOT NULL,
  tag varchar(100) NOT NULL, 
  confidence numeric);
 
