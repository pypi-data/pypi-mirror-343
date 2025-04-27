# Dia-JAX

**An experimental JAX port of Dia, the 1.6B parameter text-to-speech model from Nari Labs**

## Quickstart

**Note: Currently only recommended for experimental/development use due to memory issues**

[output.mp3](https://raw.githubusercontent.com/jaco-bro/diajax/main/assets/example_output.mp3)

```bash
pip install diajax
dia --text "[S1] Dear Jacks, to generate audio from text from any machine. (applause) [S2] Really? (screams) How! [S1] With flakes and an axe. (chuckles)"
```

```python
import diajax
model, config = diajax.load()
output = diajax.generate(model, config, text)
diajax.save(output)
```

## Acknowledgments

This project is a port of the [original Dia model](https://github.com/nari-labs/dia) by Nari Labs. We thank them for releasing their model and code, which made this port possible.

## License

This project is licensed under the same terms as the original Dia model. See [LICENSE](LICENSE) for details.
