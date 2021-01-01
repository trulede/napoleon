"""
Napoleon Sphinx Documentation - CLI
"""
import argparse
import logging
import os
import os.path
from shutil import make_archive, rmtree
from subprocess import run

import git
import requests
from setuptools import find_namespace_packages, find_packages
from sphinx.application import Sphinx

from .templates import CONF_DEFAULT, INDEX_DEFAULT, gen_template

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse arguments and resolve parameters speficied with environment
    variables. Returns an args object."""
    parser = argparse.ArgumentParser(description="Napoleon")
    parser.add_argument(
        "--git_repo",
        nargs="?",
        type=str,
        default=os.getenv("NAPOLEON_GIT_REPO", None),
        help="Repository to clone.",
    )
    parser.add_argument(
        "--git_commit",
        nargs="?",
        type=str,
        default=os.getenv("NAPOLEON_GIT_COMMIT", None),
        help="Branch, Tag or Commit SHA to checkout.",
    )
    parser.add_argument(
        "--repo_dir",
        nargs="?",
        type=str,
        default=os.getenv(
            "NAPOLEON_REPO_DIR",
            os.getenv(
                "INPUT_REPO_DIR",
                os.getenv("GITHUB_WORKSPACE", "/tmp/repo"))),
        help="Directory where the repository is located or cloned to.",
    )
    parser.add_argument(
        "--module_dirs",
        nargs="?",
        type=str,
        default=os.getenv(
            "NAPOLEON_MODULE_DIRS",
            os.getenv("INPUT_MODULE_DIRS", None)),
        help="List of modules to build API Doc, semicolon delimited.",
    )
    parser.add_argument(
        "--source_dir",
        nargs="?",
        type=str,
        default=os.getenv(
            "NAPOLEON_SOURCE_DIR",
            os.getenv("INPUT_SOURCE_DIR", "doc/source")),
        help="Location of the source dir, relative to the repo_dir.",
    )
    parser.add_argument(
        "--build_dir",
        nargs="?",
        type=str,
        default=os.getenv(
            "NAPOLEON_BUILD_DIR",
            os.getenv("INPUT_BUILD_DIR", "doc/build")),
        help="Location of the build output, relative to the repo_dir.",
    )

    parser.add_argument(
        "--archive_name",
        nargs="?",
        type=str,
        default=os.getenv(
            "NAPOLEON_ARCHIVE_NAME",
            os.getenv("INPUT_ARCHIVE_NAME", None)),
        help="",
    )
    parser.add_argument(
        "--push_url",
        nargs="?",
        type=str,
        default=os.getenv("NAPOLEON_PUSH_URL", None),
        help="",
    )
    parser.add_argument(
        "--push_user",
        nargs="?",
        type=str,
        default=os.getenv("NAPOLEON_PUSH_USER", None),
        help="",
    )
    parser.add_argument(
        "--push_token",
        nargs="?",
        type=str,
        default=os.getenv("NAPOLEON_PUSH_TOKEN", None),
        help="",
    )
    parser.set_defaults(func=lambda args: parser.print_help())
    return parser.parse_args()


def main():
    """Napoleon Sphinx Documentation - main function call."""
    args = parse_arguments()
    # Parameter hash, used for creating templates
    params = {
        "project": os.getenv("NAPOLEON_PROJECT_NAME", "Napoleon Sphinx Doc Project"),
        "copyright": os.getenv("NAPOLEON_COPYRIGHT", ""),
        "author": os.getenv("NAPOLEON_AUTHOR_NAME", ""),
        "release": "",
        "repo_dir": args.repo_dir,
    }

    # Clone
    if args.git_repo:
        logger.info("Clone from Git Repo : %s", args.git_repo)
        if os.path.isdir(args.repo_dir):
            rmtree(args.repo_dir, ignore_errors=True)
        repo = git.Repo.clone_from(args.git_repo, args.repo_dir)
        if args.git_commit:
            logger.info("Checkout Commit : %s", args.git_repo)
            repo.git.checkout(args.git_commit)
        repo_names = repo.remotes.origin.url.split(".git")[0].split("/")[-2:]
        params["project"] = os.getenv(
            "NAPOLEON_PROJECT_NAME", f"{repo_names[0]}-{repo_names[1]}"
        )
        params["release"] = repo.active_branch.name

    # Conf file
    conf_file = os.path.join(args.repo_dir, args.source_dir, "conf.py")
    logger.info("Sphinx Conf File : %s", conf_file)
    gen_template("conf.py", conf_file, CONF_DEFAULT, params)

    # Index file
    index_file = os.path.join(args.repo_dir, args.source_dir, "index.rst")
    logger.info("Sphinx Index File : %s", index_file)
    gen_template("index.rst", index_file, INDEX_DEFAULT, params)

    # API DOC
    if args.module_dirs:
        args.module_dirs = set(args.module_dirs.split(";"))
    else:
        args.module_dirs = set()
        args.module_dirs.update(find_packages(where=args.repo_dir))
        args.module_dirs.update(
            find_namespace_packages(where=args.repo_dir, exclude=["doc*", "test*"])
        )
    for module in args.module_dirs:
        logger.info("Call sphinx-apidoc for module : %s", module)
        cmd = run(
            args=[
                "sphinx-apidoc",
                "-f",
                "-o",
                f"{args.source_dir}",
                f"{module}",
            ],
            cwd=f"{args.repo_dir}",
            capture_output=True,
            check=False,
        )
        print(cmd.stdout.decode().strip())

    # Build
    build = Sphinx(
        srcdir=os.path.join(args.repo_dir, args.source_dir),
        confdir=os.path.join(args.repo_dir, args.source_dir),
        outdir=os.path.join(args.repo_dir, args.build_dir, "html"),
        doctreedir=os.path.join(args.repo_dir, args.build_dir, "doctrees"),
        buildername="html",
    )
    build.build()

    # Zip
    if not args.archive_name:
        if args.git_repo:
            args.archive_name = "__".join(
                [
                    repo_names[0],
                    repo_names[1],
                    repo.active_branch.name,
                ]
            )
        else:
            args.archive_name = f"{os.path.basename(args.repo_dir)}"
    archive_root_path = os.path.join(args.repo_dir, args.build_dir, "html")
    archive_basename = os.path.join(args.repo_dir, args.build_dir, args.archive_name)
    archive_name = os.path.join(
        args.repo_dir, args.build_dir, f"{args.archive_name}.zip"
    )
    logger.info("Create Archive : %s", archive_name)
    logger.info("   (root path) : %s", archive_root_path)
    make_archive(archive_basename, "zip", root_dir=archive_root_path)

    # Output for GitHub Actions, i.e. only when INPUT_ARCHIVE_NAME is set.
    if os.getenv("INPUT_ARCHIVE_NAME", None):
        archive_path = os.path.join(args.build_dir, f"{args.archive_name}.zip")
        print(f"::set-output name=archive_path::archive_path}")

    # Push
    if args.push_url:
        logger.info("Push File :%s", archive_name)
        logger.info("     URL  : %s", args.push_url)
        with open(archive_name) as file:
            requests.put(
                args.push_url, auth=(args.push_user, args.push_token), data=file
            )


if __name__ == "__main__":
    main()
