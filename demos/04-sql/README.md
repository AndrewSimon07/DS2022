# Working with SQL databases

Live demo. Students connect with the shared read-only `ds2022` account (password on Canvas). Schema setup and writes are done by the instructor.

## Command line tools for SQL

### CLI Setup

Confirm that `uv` is installed.

```bash
uv --version
```

If you receive an error message, follow the [uv setup instructions](../../class/03-scripting/README.md#setup).

```bash
uv tool install mycli
```

This installs `mycli` under `~/.local/bin/`. Confirm:

```bash
ls -ltr ~/.local/bin
```

To run `mycli` from any directory, check that `~/.local/bin` is on your `$PATH`:

```bash
echo $PATH
```

If it is missing, add it:

**Bash:**

```bash
echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

**Zsh:**

```bash
echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.zshrc
source ~/.zshrc
```

Confirm `mycli` works:

```bash
mycli -h
```

### Connecting to a database instance

```bash
mycli -h ds2022.cgls84scuy1e.us-east-1.rds.amazonaws.com -P 3306 -u ds2022 -p
```

The `ds2022` account can run read operations (`SHOW`, `DESCRIBE`, `SELECT`, joins). It cannot create databases or insert, update, or delete rows.

### Create a database

```sql
CREATE DATABASE restaurant;
```

### Switch to database & create a table

```sql
USE restaurant;
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(50),
    state_id INT
);
```

### Show tables

```sql
SHOW FULL TABLES;
```

Shows `employees` plus `employees_jobs`, `jobs`, and `states` (after the demo schema is loaded).

```text
┌──────────────────────┬────────────┐
│ Tables_in_restaurant │ Table_type │
├──────────────────────┼────────────┤
│ employees_jobs       │ BASE TABLE │
│ employees            │ BASE TABLE │
│ jobs                 │ BASE TABLE │
│ states               │ BASE TABLE │
└──────────────────────┴────────────┘
```

### Describe table

```sql
DESCRIBE employees;
```

```text
┌─────────────┬─────────────┬──────┬─────┬─────────┬───────┐
│ Field       │ Type        │ Null │ Key │ Default │ Extra │
├─────────────┼─────────────┼──────┼─────┼─────────┼───────┤
│ employee_id │ int         │ NO   │ PRI │ <null>  │       │
│ name        │ varchar(50) │ YES  │     │ <null>  │       │
│ state_id    │ int         │ YES  │     │ <null>  │       │
└─────────────┴─────────────┴──────┴─────┴─────────┴───────┘
```

### Create new records

```sql
INSERT INTO employees (employee_id, name, state_id)
VALUES (1, 'Alice', 26);

INSERT INTO employees (employee_id, name, state_id)
VALUES (2, 'Bob', 56);
```

### Read records

```sql
SELECT * FROM employees
WHERE name = 'Alice';
```

### Update records

```sql
UPDATE employees SET state_id = 56
WHERE name = 'Alice';
```

### Delete records

```sql
DELETE FROM employees
WHERE state_id = 56;
```

### SQL Scripts

A `.sql` file is a sequence of statements MySQL can execute in order. [restaurant.sql](./restaurant.sql) creates the `restaurant` schema and sample data. Run it from `demos/04-sql/` (or use a full path to the file). Requires a write-capable account (not `ds2022`).

**Option A: `source` inside `mycli`**

Already connected in an interactive session:

```sql
source --special restaurant.sql
```

`source` reads the file and runs each statement in the current session. `--special` is required in `mycli` so client-side commands in the file are accepted; without it the load can stop with an error. If prompted about a destructive command, that is the script’s `DROP TABLE IF EXISTS` lines.

**Option B: redirect from the shell**

No interactive session needed; `mycli` runs the file and exits:

```bash
mycli -h ds2022.cgls84scuy1e.us-east-1.rds.amazonaws.com -P 3306 -u USER -p < restaurant.sql
```

Same statements as Option A; the shell feeds the file on stdin instead of using `source`.

### Join

```sql
SELECT *
FROM employees
LEFT JOIN states ON employees.state_id = states.state_code;
```

### Join and filter

```sql
SELECT employees.name, states.home_state
FROM employees
LEFT JOIN states ON employees.state_id = states.state_code;
```

## Python and SQL

### Python Setup

```bash
mkdir -p ~/ds2022-fall-26
cd ~/ds2022-fall-26
uv init sql-class --description "SQL class examples"
cd sql-class
uv add mysql-connector-python pandas matplotlib
```


### A basic Python script

See [basic-sql.py](../../class/04-sql/basic-sql.py) (same examples as [basic-sql.ipynb](../../class/04-sql/basic-sql.ipynb), against `media.MOCK_DATA`).

Copy that example script into this project (from your clone of the course repo):

```bash
cp /path/to/DS2022/class/04-sql/basic-sql.py .
```

Set connection environment variables (password on Canvas), then run:

```bash
export DBHOST='ds2022.cgls84scuy1e.us-east-1.rds.amazonaws.com'
export DBUSER='ds2022'
export DBPASS='YOUR_PASSWORD'
export DB='media'

uv run python basic-sql.py
```

`uv run` uses the project’s virtual environment (including `mysql-connector-python`). The script must live in the current project directory, or you pass a path: `uv run python /path/to/basic-sql.py`.

### Python notebook

Example: [basic-sql.ipynb](../../class/04-sql/basic-sql.ipynb)

The notebook queries the `media` database (`MOCK_DATA`), so use the same `sql-class` project and add the extra packages it imports:

```bash
cd ~/ds2022-fall-26/sql-class
uv add mysql-connector-python pandas matplotlib jupyter
cp /path/to/DS2022/class/04-sql/basic-sql.ipynb .
uv run jupyter lab basic-sql.ipynb
```

In the notebook’s connection cell, set `DBUSER` / `DBPASS` for the read-only `ds2022` account and `DB = "media"`. Then run the cells in order.
