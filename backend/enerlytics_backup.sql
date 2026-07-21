--
-- PostgreSQL database dump
--

\restrict kNO9TvIblz4dSa5M0ffcKk2CWkrLiqzY2puOZ0RAHGkL1dsKNoorjvJ0jyIsuyU

-- Dumped from database version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: enerlytics
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO enerlytics;

--
-- Name: reports; Type: TABLE; Schema: public; Owner: enerlytics
--

CREATE TABLE public.reports (
    community character varying(100) NOT NULL,
    outage boolean NOT NULL,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.reports OWNER TO enerlytics;

--
-- Name: reports_id_seq; Type: SEQUENCE; Schema: public; Owner: enerlytics
--

CREATE SEQUENCE public.reports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reports_id_seq OWNER TO enerlytics;

--
-- Name: reports_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: enerlytics
--

ALTER SEQUENCE public.reports_id_seq OWNED BY public.reports.id;


--
-- Name: reports id; Type: DEFAULT; Schema: public; Owner: enerlytics
--

ALTER TABLE ONLY public.reports ALTER COLUMN id SET DEFAULT nextval('public.reports_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: enerlytics
--

COPY public.alembic_version (version_num) FROM stdin;
a12363614ed5
\.


--
-- Data for Name: reports; Type: TABLE DATA; Schema: public; Owner: enerlytics
--

COPY public.reports (community, outage, id, created_at, updated_at) FROM stdin;
\.


--
-- Name: reports_id_seq; Type: SEQUENCE SET; Schema: public; Owner: enerlytics
--

SELECT pg_catalog.setval('public.reports_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: enerlytics
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: reports reports_pkey; Type: CONSTRAINT; Schema: public; Owner: enerlytics
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_pkey PRIMARY KEY (id);


--
-- Name: ix_reports_id; Type: INDEX; Schema: public; Owner: enerlytics
--

CREATE INDEX ix_reports_id ON public.reports USING btree (id);


--
-- PostgreSQL database dump complete
--

\unrestrict kNO9TvIblz4dSa5M0ffcKk2CWkrLiqzY2puOZ0RAHGkL1dsKNoorjvJ0jyIsuyU

