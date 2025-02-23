-- create the table tasks
CREATE TABLE IF NOT EXISTS public.tasks
(
    id serial,
	fechacreacion timestamp,
 	fechamodificacion timestamp,
    selected bool,
    titulo varchar,
    estado varchar,
    prioridad varchar,
    PRIMARY KEY (id)
);

-- Data
INSERT INTO public.tasks (fechacreacion,fechamodificacion,selected,titulo,estado,prioridad) VALUES
	 ('2025-01-09 16:52:43','2025-01-09 16:52:43',True,'Documentation','Backlog','Low'),
	 ('2025-01-09 16:52:43','2025-01-09 16:52:43',True,'Bug','Todo','Medium');