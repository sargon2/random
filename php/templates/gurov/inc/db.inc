<?
mysql_pconnect(':/tmp/mysql.sock', 'ramcon2', 'r40asdf34234a');
mysql_select_db('RAMCON2');

function fix_reg() {
        mysql_query("drop table register_temp");
        mysql_query("select @num:=0");
        mysql_query("create table register_temp as select *, @num:=@num+1 as spotid from register where active order by confirmed desc, timestamp ");
}


?>
