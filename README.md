# PRJCTR HSA HOMEWORK 9

This project contains solution for 9th prjctr hometask. 
It includes mariadb container, simple python web app written with fastapi,
TIG stack for monitoring resources during tests. The main goal is to test 
the database operation with 40m+ randomly generated users table. Tests include
selecting operations performance without index and with btree and hash indexes, 
also inserting in the same configurations and with different flush log settings. 
Results are available below.

## Prerequisites

[Docker](https://www.docker.com/products/docker-desktop/) installation.

[siege](https://linux.die.net/man/1/siege) installation for running tests.

## Setup and running

* Check `./app` folder for a web server.
* Check `./conf.d` folder for a mariadb configuration. The same config was 
used across different tests, only `innodb_flush_log_at_trx_commit` variable
was changed during insert tests.
* Check `./initdb.d` folder for the entrypoint SQLs.
* Check `./siege_urls.txt` for the `siege` test URLs.

To run the app:

1. `docker-compose build`
2. `docker-compose up -d`
3. (optional) Check `./app/settings.py` to configure the tests and web app.
4. (optional) Run the seeds: `docker-compose run app python seed.py`
5. Run tests: `siege -c100 -d1 -i -q -t180s --file=./siege_urls.txt --log=siege.log`.
This command was used for almost all the tests and it runs multiple requests 
with 100 connections for 180 seconds.

## Results

Users table definition

![users table definition](./images/users_table_def.png)

Users count

![total users count](./images/total_users_count.png)

### No index

Without index, I had a very fast insert operations which almost 
aren't depend on log trx commit setting. And a very poor time for selecting
operations. Moreover, queries like `WHERE birth_date > ?` or 
`WHERE birth_date < ?` were often timed out.

#### Reading

Web stats

![web stats](./images/no_index/no_index_reading_web_stats.png)

System stats

![system stats](./images/no_index/no_index_reading_system_stats.png)

MySQL stats

![mysql stats](./images/no_index/no_index_reading_mysql_stats.png)

MySQL queries stats

![mysql queries stats](./images/no_index/no_index_reading_mysql_queries.png)

MySQL buffer stats

![mysql buffer stats](./images/no_index/no_index_reading_mysql_buffer.png)

#### Inserts (`innodb_flush_log_at_trx_commit = 0`)

Web stats

![web stats](./images/no_index/no_index_writing_0_web_stats.png)

System stats

![system stats](./images/no_index/no_index_writing_0_system_stats.png)

MySQL log writes stats

![mysql log writes stats](./images/no_index/no_index_writing_0_mysql_log_writes.png)

#### Inserts (`innodb_flush_log_at_trx_commit = 1`)

MySQL log writes stats

![mysql log writes stats](./images/no_index/no_index_reading_mysql_log_writes.png)

#### Inserts (`innodb_flush_log_at_trx_commit = 2`)

Web stats

![web stats](./images/no_index/no_index_writing_2_web_stats.png)

System stats

![system stats](./images/no_index/no_index_writing_2_system_stats.png)

MySQL stats

![mysql stats](./images/no_index/no_index_writing_2_mysql_stats.png)

MySQL buffer stats

![mysql buffer stats](./images/no_index/no_index_writing_2_mysql_buffer.png)

MySQL log writes stats

![mysql log writes stats](./images/no_index/no_index_writing_2_mysql_log_writes.png)

### Btree index

Indexes were significantly changed the reading operations time. But 
insert speed was reduced in comparison with no index. Also, the 
creating index operation is a very expensive one.

Index creation

![btree_index_creation.png](images%2Fbtree%2Fbtree_index_creation.png)

#### Reading

Web stats

![btree_reading_web_stats.png](images%2Fbtree%2Fbtree_reading_web_stats.png)

System stats

![btree_reading_system_stats.png](images%2Fbtree%2Fbtree_reading_system_stats.png)

Even I had swap usage percentage :)

![btree_reading_swap_stats.png](images%2Fbtree%2Fbtree_reading_swap_stats.png)

MySQL stats

![btree_reading_mysql_stats.png](images%2Fbtree%2Fbtree_reading_mysql_stats.png)

MySQL queries

![btree_reading_mysql_queries.png](images%2Fbtree%2Fbtree_reading_mysql_queries.png)

MySQL buffer 

![btree_reading_mysql_buffer.png](images%2Fbtree%2Fbtree_reading_mysql_buffer.png)

#### Inserts (`innodb_flush_log_at_trx_commit = 0`)

Web stats

![btree_writing_0_web_stats.png](images%2Fbtree%2Fbtree_writing_0_web_stats.png)

System stats

![btree_writing_0_system_stats.png](images%2Fbtree%2Fbtree_writing_0_system_stats.png)

MySQL buffer stats

![btree_writing_0_mysql_buffer.png](images%2Fbtree%2Fbtree_writing_0_mysql_buffer.png)

MySQL log writes stats

![btree_writing_0_mysql_log_writes.png](images%2Fbtree%2Fbtree_writing_0_mysql_log_writes.png)

#### Inserts (`innodb_flush_log_at_trx_commit = 1`)

Web stats

![btree_writing_1_web_stats.png](images%2Fbtree%2Fbtree_writing_1_web_stats.png)

MySQL buffer stats

![btree_writing_1_mysql_buffer.png](images%2Fbtree%2Fbtree_writing_1_mysql_buffer.png)

MySQL log writes stats

![btree_writing_1_mysql_log_writes.png](images%2Fbtree%2Fbtree_writing_1_mysql_log_writes.png)

#### Inserts (`innodb_flush_log_at_trx_commit = 2`)

Web stats

![btree_writing_2_web_stats.png](images%2Fbtree%2Fbtree_writing_2_web_stats.png)

MySQL buffer stats

![btree_writing_2_mysql_buffer.png](images%2Fbtree%2Fbtree_writing_2_mysql_buffer.png)

MySQL buffer pages stats

![btree_writing_2_mysql_buffer_pages.png](images%2Fbtree%2Fbtree_writing_2_mysql_buffer_pages.png)

MySQL log writes stats

![btree_writing_2_mysql_log_writes.png](images%2Fbtree%2Fbtree_writing_2_mysql_log_writes.png)

### Hash index

To enable hash index in mariadb >=10.6 a special configuration setting needs to be added.

`innodb_adaptive_hash_index = 0`

Index creation

![hash_index_creation.png](images%2Fhash%2Fhash_index_creation.png)

#### Reading

Web stats

![hash_reading_web_stats.png](images%2Fhash%2Fhash_reading_web_stats.png)

System stats

![hash_reading_system_stats.png](images%2Fhash%2Fhash_reading_system_stats.png)

MySQL stats

![hash_reading_mysql_stats.png](images%2Fhash%2Fhash_reading_mysql_stats.png)

MySQL queries

![hash_reading_mysql_queries.png](images%2Fhash%2Fhash_reading_mysql_queries.png)

MySQL buffer stats

![hash_reading_mysql_buffer.png](images%2Fhash%2Fhash_reading_mysql_buffer.png)

MySQL buffer requests stats

![hash_reading_mysql_buffer_requests.png](images%2Fhash%2Fhash_reading_mysql_buffer_requests.png)

#### Inserts (`innodb_flush_log_at_trx_commit = 0`)

Web stats

![hash_writing_0_web_stats.png](images%2Fhash%2Fhash_writing_0_web_stats.png)

System stats

![hash_writing_0_system_stats.png](images%2Fhash%2Fhash_writing_0_system_stats.png)

MySQL buffer stats

![hash_writing_0_mysql_buffer.png](images%2Fhash%2Fhash_writing_0_mysql_buffer.png)

MySQL log writes stats

![hash_writing_0_mysql_log_writes.png](images%2Fhash%2Fhash_writing_0_mysql_log_writes.png)

#### Inserts (`innodb_flush_log_at_trx_commit = 1`)

Web stats

![hash_writing_1_web_stats.png](images%2Fhash%2Fhash_writing_1_web_stats.png)

System stats

![hash_writing_1_system_stats.png](images%2Fhash%2Fhash_writing_1_system_stats.png)

MySQL buffer stats

![hash_writing_1_mysql_buffer.png](images%2Fhash%2Fhash_writing_1_mysql_buffer.png)

MySQL log writes stats

![hash_writing_1_mysql_log_writes.png](images%2Fhash%2Fhash_writing_1_mysql_log_writes.png)

#### Inserts (`innodb_flush_log_at_trx_commit = 2`)

Web stats

![hash_writing_2_web_stats.png](images%2Fhash%2Fhash_writing_2_web_stats.png)

System stats

![hash_writing_2_system_stats.png](images%2Fhash%2Fhash_writing_2_system_stats.png)

MySQL buffer stats

![hash_writing_2_mysql_buffer.png](images%2Fhash%2Fhash_writing_2_mysql_buffer.png)

MySQL log writes stats

![hash_writing_2_mysql_log_writes.png](images%2Fhash%2Fhash_writing_2_mysql_log_writes.png)

---

More images with stats during different setups can be found in `./images` folder.
