# Building Kopano4UCS

To have access to the UCS linter these packages should be build on directly on an UCS system. The easist way for a third party to do this us utilising the [openSUSE Build Service](https://build.opensuse.org).  An example project which can be "branched" is https://build.opensuse.org/package/show/home:zfbartels/kopano4ucs.

The following command performs a local build through the osc command line client and puts the resulting packages into the current directory:

```
$ osc build Univention_4.3 kopano4ucs.dsc -k .
```
