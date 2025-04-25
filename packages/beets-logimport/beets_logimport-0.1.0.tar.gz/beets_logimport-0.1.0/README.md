# LogImport plugin for Beets

This [beets] plugin adds logging of the destination paths when  you import tracks.

For this add the `logimport` plugin to your config. Then the destination paths of your imported tracks are logged. 

These are logged by default under the `INFO` level. This logging level is _for imports_ only emitted with the `--verbose` option.

If you want to see the destination paths without `--verbose`, you can set `logimport`'s configuration option `atlevel`:

```
logimport:
    atlevel: warning
```

  [beets]: https://beets.io
