CREATE TABLE organizations
(
  id serial,
  organization character(80),
  faculty character(80),
  studgroup character(20),
  tag character(30)
);

CREATE TABLE schedule
(
  id serial,
  tag character(30),
  day character(10),
  "number" smallint,
  type smallint,
  "startTime" time without time zone,
  "endTime" time without time zone,
  title character(100),
  classroom character(20),
  lecturer character(50)
);

CREATE TABLE users
(
  type character(2),
  id integer,
  name character(30),
  username character(30),
  "scheduleTag" character(30),
  auto_posting_time time without time zone,
  is_today boolean
);


CREATE TABLE public.reports
(
  type character(2),
  report_id serial,
  user_id integer,
  report text,
  date date
)