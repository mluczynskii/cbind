from dataclasses import dataclass

@dataclass
class Function:
  header: str
  instructions: list[str]

  def __str__(self) -> str:
    body = "\n".join([f"{instr};" for instr in self.instructions])
    return f"{self.header} {{\n{body} \n}}"