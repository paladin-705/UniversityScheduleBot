CREATE TABLE IF NOT EXISTS organizations
(
  id serial,
  organization character varying(80),
  faculty character varying(80),
  studgroup character varying(50),
  tag character(30) PRIMARY KEY
);

CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX IF NOT EXISTS trgm_idx ON organizations USING GIN (lower(organization || ' ' || faculty || ' ' || studgroup) gin_trgm_ops);

CREATE TABLE IF NOT EXISTS schedule
(
  id serial,
  tag character(30),
  day character varying(10),
  "number" smallint,
  type smallint,
  "startTime" time without time zone,
  "endTime" time without time zone,
  title character varying(100),
  classroom character varying(100),
  lecturer character varying(100),
  PRIMARY KEY (tag, day, number, type),
  CONSTRAINT schedule_fkey FOREIGN KEY (tag)
	REFERENCES organizations (tag) MATCH SIMPLE
	ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS examinations
(
  tag character(30),
  title character varying(100),
  classroom character varying(100),
  lecturer character varying(100),
  day date,
  CONSTRAINT examinations_fkey FOREIGN KEY (tag)
	REFERENCES organizations (tag) MATCH SIMPLE
	ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users
(
  type character(3),
  id bigint,
  name character varying(30),
  username character varying(30),
  "scheduleTag" character(30),
  auto_posting_time time without time zone,
  is_today boolean,
  registration_timestamp timestamp with time zone DEFAULT now(),
  PRIMARY KEY (type, id),
  CONSTRAINT users_fkey FOREIGN KEY ("scheduleTag")
      REFERENCES organizations (tag) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE OR REPLACE VIEW users_vw AS
 SELECT users.type,
    users.id,
    organizations.organization,
    organizations.faculty,
    organizations.studgroup,
    users.auto_posting_time,
    users.is_today,
    users.registration_timestamp
   FROM users
     JOIN organizations ON users."scheduleTag" = organizations.tag
 ORDER BY organizations.studgroup;

CREATE TABLE IF NOT EXISTS reports
(
  type character(3),
  report_id serial PRIMARY KEY,
  user_id integer,
  report text,
  date date
);

CREATE TABLE IF NOT EXISTS api_users
(
  id serial PRIMARY KEY,
  username character varying(50),
  pw_hash character(60)
)
