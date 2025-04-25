#!/usr/bin/env python3

import argparse
import importlib.resources
import os
from configparser import ConfigParser
from pprint import pprint

from querycraft.LRS import LRS
from querycraft.SQL import SQL
from querycraft.tools import existFile
from querycraft.SQLException import SQLQueryException
from querycraft.Database import *

def sbs(sql, verbose=False):
    if verbose:
        print(f"Bonjour {os.getlogin()} !")
        print('==================================================================================================')
        print('======================================== Requête à analyser ======================================')
        print('==================================================================================================')
        print("--- Schéma de la base ---")
        sql.printDBTables()
        print('--- Requête à exécuter ---')
        print(sql)
        print('--- Table à obtenir ---')
        print(sql.getPLTable())
        print('==================================================================================================')
        print('========================================== Pas à pas =============================================')
    sql.sbs()
    if verbose: print('fin')


def getQuery(args):
    if args.file:
        sqlTXT = ''
        with open(args.file, 'r') as f:
            sqlTXT += f.read()
    elif args.sql:
        sqlTXT = args.sql
    else:
        sqlTXT = ''
    return sqlTXT


def stdArgs(parser):
    #parser.add_argument('--debug', help='debug mode', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true', default=False)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-b', '--describe', help='DB Schema', action='store_true', default=False)
    group.add_argument('-f', '--file', help='sql file' )
    group.add_argument('-s', '--sql', type=str, help='sql string')

    parser.add_argument('--lrs', help='use en Veracity lrs', action='store_true', default=False)
    parser.add_argument('--lrs-user', help=f'lrs user (by default toto)', default='toto')  # 'desmontils-e')
    parser.add_argument('--lrs-password', help='lrs password (by default toto)', default='toto')
    parser.add_argument('--lrs-endpoint', help=f'lrs endpoint (by default http://local.veracity.it/querycraft/xapi/)',
                        default='http://local.veracity.it/querycraft/xapi/')  # 'localhost')
    return parser

def dbConnectArgs(parser, defaultPort, defaultHost='localhost', defaultUser='desmontils-e'):
    parser.add_argument('-d', '--db', help='database name', required=True)
    parser.add_argument('-u', '--user', help=f'database user (by default {defaultUser})',
                        default=defaultUser)  # 'desmontils-e')
    parser.add_argument('-p', '--password', help='database password', default='')
    parser.add_argument('--host', help=f'database host (by default {defaultHost})', default=defaultHost)  # 'localhost')
    parser.add_argument('--port', help=f'database port (by default {defaultPort})', default=defaultPort)  # '5432')


def doSBS(db, dbtype, dbname, sqlTXT, debug, verbose, lrs=None):
    try:
        cfg = readConfigFile()

        # IA configuration
        model = cfg['IA']['model']
        if debug: print('Model : ', model)
        SQLQueryException.set_model(model)

        # LRS configuration
        if lrs:
            lrs.setContextSBS()
        sql = SQL(db=db, dbtype=dbtype, debug=debug, verbose=verbose)
        sql.setSQL(sqlTXT)
        if lrs: lrs.sendSBSExecute(dbtype, dbname, sqlTXT)

        # Lancement du programme
        try:
            sbs(sql, verbose)  # Pas à pas
            if lrs: lrs.sendSBSpap(dbtype, dbname, sqlTXT)
        except Exception as e:
            # LRS : envoie du statement
            if lrs: lrs.sendSBSpap(dbtype, dbname, sqlTXT, error=e)
            print(f'Erreur SBS : {e}')
    except Exception as e:
        print(f"Erreur doSBS = {e}")
        # LRS : envoie du statement
        if lrs: lrs.sendSBSExecute(dbtype, dbname, sqlTXT, error=e)
        exit()


def mysql():
    parser = argparse.ArgumentParser(
        description="Effectue l'exécution pas à pas d'une requête sur MySQL\n (c) E. Desmontils, Nantes Université, 2024")
    dbConnectArgs(parser, '3306', defaultHost='localhost')
    stdArgs(parser)
    args = parser.parse_args()
    debug = False
    verbose = args.verbose
    #if debug:
    #    print('Infos BD : ', type, args.user, args.password, args.host, args.port, args.db)
    if args.describe:
        # Affichage des tables de la BD
        try:
            db = DBMySQL(db=(args.user, args.password, args.host, args.db), debug=False, verbose=args.verbose)
            print(db.tables2string())
            exit(0)
        except Exception as e:
            print(f'Erreur Describe MySQL : {e}')
            exit(1)
    sqlTXT = getQuery(args)
    if args.lrs:
        doSBS((args.user, args.password, args.host, args.db), 'mysql', args.db, sqlTXT, False, args.verbose,
              LRS(args.lrs_endpoint, args.lrs_user, args.lrs_password, debug=args.debug))
    else:
        doSBS((args.user, args.password, args.host, args.db), 'mysql', args.db, sqlTXT, False, args.verbose)


def pgsql():
    parser = argparse.ArgumentParser(
        description="Effectue l'exécution pas à pas d'une requête sur PostgreSQL\n (c) E. Desmontils, Nantes Université, 2024")
    dbConnectArgs(parser, '5432', defaultHost='localhost')
    stdArgs(parser)
    args = parser.parse_args()
    #if args.debug:
    #    print('Infos BD : ', type, args.user, args.password, args.host, args.port, args.db)
    if args.describe:
        # Affichage des tables de la BD
        try:
            db = DBPGSQL(db=f"dbname={args.db} user={args.user} password={args.password} host={args.host} port={args.port}", debug=False, verbose=args.verbose)
            print(db.tables2string())
            exit(0)
        except Exception as e:
            print(f'Erreur Describe PostgreSQL : {e}')
            exit(1)
    sqlTXT = getQuery(args)
    if args.lrs:
        doSBS(f"dbname={args.db} user={args.user} password={args.password} host={args.host} port={args.port}", 'pgsql',
              args.db, sqlTXT, False, args.verbose,
              LRS(args.lrs_endpoint, args.lrs_user, args.lrs_password, debug=args.debug))
    else:
        doSBS(f"dbname={args.db} user={args.user} password={args.password} host={args.host} port={args.port}", 'pgsql',
              args.db, sqlTXT, False, args.verbose)

def sqlite():
    parser = argparse.ArgumentParser(
        description="Effectue l'exécution pas à pas d'une requête sur SQLite\n (c) E. Desmontils, Nantes Université, 2024")
    parser.add_argument('-d', '--db', help='database name', required=True)
    parser = stdArgs(parser)
    args = parser.parse_args()
    if not (existFile(args.db)):
        if args.verbose: print(f'database file not found : {args.db}')
        package_files = importlib.resources.files("querycraft.data")
        if args.verbose: print(f'trying to search in default databases')
        if not (existFile(package_files / args.db)):
            print(f'database file not found')
            exit(1)
        else:
            args.db = package_files / args.db
            if args.verbose: print('database exists')
    else:
        if args.verbose: print('database exists')
    #if args.debug:
    #    print('Infos BD : ', type, args.user, args.password, args.host, args.port, args.db)
    if args.describe:
        # Affichage des tables de la BD
        try:
            db = DBSQLite(db=str(args.db),debug=False,verbose=args.verbose)
            print(db.tables2string())
            exit(0)
        except Exception as e:
            print(f'Erreur Describe SQLite : {e}')
            exit(1)
    sqlTXT = getQuery(args)
    if args.lrs:
        doSBS(args.db, 'sqlite', args.db, sqlTXT, False, args.verbose,
              LRS(args.lrs_endpoint, args.lrs_user, args.lrs_password, debug=args.debug))
    else:
        doSBS(args.db, 'sqlite', args.db, sqlTXT, False, args.verbose)

def readConfigFile():
    # lecture du fichier de configuration
    cfg = ConfigParser()
    with importlib.resources.open_text("querycraft.config", "config-sbs.cfg") as fichier:
        cfg.read_file(fichier)
    return cfg

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lrs', help='use en Veracity lrs', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true', default=False)
    parser.add_argument('--debug', help='debug mode', action='store_true', default=False)
    parser.add_argument('-d', '--db', help='database file (sqlite) or name (others)', default=None)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help='sql file')
    group.add_argument('-s', '--sql', type=str, help='sql string', default="")
    group.add_argument('-b', '--describe', help='DB Schema', action='store_true', default=False)

    args = parser.parse_args()
    sqlTXT = getQuery(args)

    # db = Database.getPGSQLDB(dbcon='dbname=cours')
    # db = Database.getPGSQLDB(dbcon='dbname=cours')
    # db = Database.getSQLiteDB(dbcon='./static/bdd/cours/cours.db')
    # db = Database.getSQLiteDB(dbcon='./static/bdd/cours/cours.db')
    # db = Database.getDB('./static/bdd/cours/cours.db','sqlite')
    # exit()

    # ==================================================
    # === Gestion de la configuration =================
    # ==================================================
    cfg = readConfigFile()

    onLRS = args.lrs
    # Debug ?
    debug = cfg.getboolean('Autre', 'debug') or args.debug
    verbose = cfg.getboolean('Autre', 'verbose') or args.verbose
    if debug:
        print("Mode debug activé")
    package_files = importlib.resources.files("querycraft.data")
    # Database configuration
    if args.db:
        if args.db.endswith('.db'):
            if not (existFile(args.db)):
                if args.verbose:
                    print(f'database file not found : {args.db}')
                    print(f'trying to search in default databases')
                if not (existFile(package_files / args.db)):
                    print(f'database file not found')
                    exit(1)
                else:
                    args.db = package_files / args.db
                    if args.verbose: print('database exists')
            else:
                if args.verbose: print('database exists')
            database = args.db
            if debug: print(f"SQLite database from parameter : {database}")
            type = 'sqlite'
            username = None
            password = None
            host = None
            port = None
        else:
            database = args.db
            if debug: print(f"PGSQL database from parameter : {database}")
            type = 'pgsql'  # Database configuration
            username = 'postgres'
            password = ''
            host = 'localhost'
            port = '5432'
    else:
        type = cfg['Database']['type']
        if type == 'sqlite':
            if debug: print(f"SQLite database from config file : {cfg['Database']['database']}")
            database = package_files / cfg['Database'][
                'database']  # importlib.resources.resource_filename("querycraft.data", cfg['Database']['database'])
            username = None
            password = None
            host = None
            port = None
        else:
            if debug: print(f"{type} database from config file : {cfg['Database']['database']}")
            username = cfg['Database']['username']
            password = cfg['Database']['password']
            host = cfg['Database']['host']
            port = cfg['Database']['port']
            database = cfg['Database']['database']

    # xAPI configuration
    if onLRS:
        lrs = LRS(cfg['LRS']['endpoint'], cfg['LRS']['username'], cfg['LRS']['password'], debug=debug)
        lrs.setContextSBS()

    # IA configuration
    model = cfg['IA']['model']
    if debug: print('Model : ', model)
    SQLQueryException.set_model(model)

    if debug:
        print('Infos BD : ', type, username, password, host, port, database)

    try:
        try:
            if type is None:
                raise Exception("Configuration non fournie")
            if type == 'sqlite':
                if args.describe:
                    # Affichage des tables de la BD
                    try:
                        db = DBSQLite(db=database, debug=False, verbose=args.verbose)
                        print(f"{type}\n{db.tables2string()}")
                        exit(0)
                    except Exception as e:
                        print(f"Erreur Describe SQLite : {e}")
                        exit(1)
                sql = SQL(db=database, dbtype='sqlite', debug=debug, verbose=verbose)
            elif type == 'pgsql': # f"dbname={database} user={username} password={password} host={host} port={port}"
                if args.describe:
                    # Affichage des tables de la BD
                    try:
                        db = DBPGSQL(db=f"dbname={database} user={username} password={password} host={host} port={port}", debug=False, verbose=args.verbose)
                        print(f"{type}\n{db.tables2string()}")
                        exit(0)
                    except Exception as e:
                        print(f"Erreur Describe PostgreSQL : {e}")
                        exit(1)
                sql = SQL(f"dbname={database} user={username} password={password} host={host} port={port}", dbtype='pgsql', debug=debug, verbose=verbose)
            elif type == 'mysql': # (username, password, host ,database) # port ????
                if args.describe:
                    # Affichage des tables de la BD
                    try:
                        db = DBMySQL(db=(username, password, host ,database), debug=False, verbose=args.verbose)
                        print(f"{type}\n{db.tables2string()}")
                        exit(0)
                    except Exception as e:
                        print(f"Erreur Describe MySQL : {e}")
                        exit(1)
                sql = SQL(db=(username, password, host ,database), dbtype='mysql', debug=debug, verbose=verbose)
            else:
                raise Exception("Base de données non supportée")

            sql.setSQL(sqlTXT)

            # LRS : envoie du statement
            if onLRS: lrs.sendSBSExecute(type, database, sqlTXT)

        except Exception as e:
            pprint(e)
            # LRS : envoie du statement
            if onLRS: lrs.sendSBSExecute(type, database, sqlTXT, error=e)
            exit()

        sbs(sql, verbose)  # Pas à pas

        if onLRS: lrs.sendSBSpap(type, database, sqlTXT)

    except Exception as e:
        # LRS : envoie du statement
        if onLRS: lrs.sendSBSpap(type, database, sqlTXT, e)
        print(f'Erreur SBS : {e}')


if __name__ == '__main__':
    main()
