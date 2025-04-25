# Installation

Generally, extensions need to be installed into the same Python environment Salt uses.

:::{tab} State
```yaml
Install Salt Test-salt-winrepo extension:
  pip.installed:
    - name: saltext-test-salt-winrepo
```
:::

:::{tab} Onedir installation
```bash
salt-pip install saltext-test-salt-winrepo
```
:::

:::{tab} Regular installation
```bash
pip install saltext-test-salt-winrepo
```
:::

:::{hint}
Saltexts are not distributed automatically via the fileserver like custom modules, they need to be installed
on each node you want them to be available on.
:::
