#!/usr/bin/env python

import psycopg2

from prettytable import PrettyTable


def print_results(header, results):
    table = PrettyTable(header)
    for row in results:
        table.add_row(row)
    print table


def get_most_popular_articles():
    """Return 3 most popular articles, most popular first."""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("select articles.title, article_counter.count "
              "from articles, article_counter "
              "where article_counter.slug = articles.slug "
              "order by article_counter.count "
              "desc limit 3")

    articles = c.fetchall()
    db.close()
    print_results(['Article', 'Views'], articles)


def get_most_popular_authors():
    """Return most popular article authors of all time, most popular first."""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("select authors.name, sum(article_counter.count) as count "
              "from articles "
              "join article_counter on articles.slug = article_counter.slug "
              "join authors on authors.id = articles.author "
              "group by authors.name "
              "order by count desc")

    authors = c.fetchall()
    db.close()
    print_results(['Authors', 'Views'], authors)


def get_erroneous_days():
    """Return days when more than 1% of requests lead to errors."""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("select requestcount.day as errordate, "
              "requestcount.errorRequest*100/requestcount.totalRequests "
              "as percent "
              " from(select log1.day, log1.totalRequests, log2.errorRequest "
              "from (select CAST(time AS DATE) as day, count(time) "
              "as totalRequests "
              "from log group by day) log1 "
              "full outer join (select CAST(time AS DATE) as day, count(time) "
              "as errorRequest from log "
              "where status='404 NOT FOUND' "
              "group by day) log2 "
              "on log1.day = log2.day) requestcount "
              "where "
              "requestcount.errorRequest*100/requestcount.totalRequests >= 1")

    errdays = c.fetchall()
    db.close()
    print_results(['Date', 'Views'], errdays)


def main():
    print '3 MOST POPULAR ARTICLES OF ALL TIME'

    get_most_popular_articles()
    print('\n\n')

    print 'MOST POPULAR AUTHORS OF ALL TIME'
    get_most_popular_authors()
    print('\n\n')

    print 'DAYS WITH ERROR % >1'
    get_erroneous_days()
    print('\n\n')


if __name__ == '__main__':
    main()
