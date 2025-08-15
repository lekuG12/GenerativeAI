from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun
)


class CalculatorTool(BaseTool):
    name = 'Calculator'
    description = 'A tool to perform basic arithmetic operations like addition, subtraction, multiplication and division.'

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            return str(eval(query))
        except Exception as e:
            return f"Error in calculation: {str(e)}"
        
    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        
        try:
            return str(eval(query))
        except Exception as e:
            return f"Error in calculation: {str(e)}"
        