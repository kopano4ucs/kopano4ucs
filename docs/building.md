# Building Kopano4UCS

To have access to the UCS linter these packages should be build on directly on an UCS system. The easiest way for a third party to do this us utilizing the [openSUSE Build Service](https://build.opensuse.org).  An example project which can be "branched" is https://build.opensuse.org/package/show/home:zfbartels/kopano4ucs.

The following command performs a local build through the osc command line client and puts the resulting packages into the current directory:

```bash
$ osc build Univention_4.4 kopano4ucs.dsc -k .
```

## Copy local state to https://build.opensuse.org/

```bash
osc copypac -t https://api.opensuse.org kopano4ucs kopano4ucs home:zfbartels kopano4ucs
```
