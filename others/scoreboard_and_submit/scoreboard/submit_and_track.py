#!/usr/bin/env python3
"""SinkhornNorm: dry-run, GET-only doctor/resume/reconcile, or one submission."""
import argparse
import json
import sinkhorn_workflow as workflow

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--account',help='Explicit configured memberN; never rotates accounts')
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--dry-run',action='store_true',help='Offline package validation; no login/network/device/POST')
    mode.add_argument('--doctor',action='store_true',help='Live target/project checks using GET only')
    mode.add_argument('--resume',metavar='SUBMISSION_ID',help='Continue querying an existing submission; no POST')
    mode.add_argument('--reconcile',metavar='JOB_ID',help='Resolve an uncertain POST with GET only')
    parser.add_argument('--daily-limit',type=int,help='Optional human-selected local daily cap; server limit remains authoritative')
    parser.add_argument('--repeat',action='store_true',help='Allow a deliberate repeat of already-submitted source')
    args=parser.parse_args()
    if not args.dry_run and not args.doctor and not args.account:
        parser.error('An explicit --account is required for submit/resume/reconcile')
    try:
        if args.dry_run:
            result=workflow.dry_run()
        elif args.doctor:
            result=workflow.doctor(args.account)
        elif args.resume:
            result=workflow.resume(args.account,args.resume)
        elif args.reconcile:
            result=workflow.reconcile(args.account,args.reconcile)
        else:
            result=workflow.submit(args.account,args.daily_limit,args.repeat)
        print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    except (Exception,KeyboardInterrupt) as error:
        parser.exit(1,'Stopped: '+str(error)+'\n')

if __name__=='__main__':
    main()
