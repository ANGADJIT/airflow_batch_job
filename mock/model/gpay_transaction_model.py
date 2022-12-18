from dataclasses import dataclass,field
from enum import Enum
from random import randint,random,sample,choice
from datetime import datetime
from string import ascii_lowercase,ascii_uppercase,digits

# This enum represents the Payment Status
class PAYMENT_STATUS(Enum):
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    PENDING = 'PENDING' 

    def __str__(self) -> str:
        return self.value

# This is Gpay Mock Transaction model
@dataclass(frozen=True,order=True)
class GPayTransaction:

    def __assign_mock_transaction_value() -> float:
        return round((randint(1,6) * randint(1,10000)) + random(),2)

    def __assign_mock_transaction_id() -> str:
        random_key: str = ''.join(sample(f'{ascii_lowercase}{ascii_uppercase}{digits}',k=12))

        return f'GPAY/{random_key}'
    
    def __assign_bank_name() -> str:
        with open('mock/data/banks.txt') as banks_txt:
            banks: list[str] = banks_txt.readlines()

            return choice([bank.strip() for bank in banks])
    
    def __assign_indian_state() -> str:
        with open('mock/data/states.txt') as states_txt:
            states: list[str] = states_txt.readlines()

            return choice([state.strip() for state in states])

    def __assign_hour() -> int:
        return datetime.now().hour

    def __assign_minute() -> int:
        return datetime.now().minute
    
    def __assign_payment_status() -> str:
        return str(choice(list(PAYMENT_STATUS)))

    def __assign_transaction_time() -> int:
        return randint(1,11)

    __id: str = field(default_factory=__assign_mock_transaction_id)
    __amount: float = field(default_factory=__assign_mock_transaction_value)
    __bank_name: str = field(default_factory=__assign_bank_name)
    __ind_state: str = field(default_factory=__assign_indian_state)
    __hour: int = field(default_factory=__assign_hour)
    __minutes: int = field(default_factory=__assign_minute)
    __status: PAYMENT_STATUS = field(default_factory=__assign_payment_status)
    __transaction_time_in_seconds: int = field(default_factory=__assign_transaction_time)

    def __str__(self) -> str:
        record_str: str = f'{self.__id},{self.__amount},{self.__bank_name},{self.__ind_state},{self.__hour},{self.__minutes},{self.__status},{self.__transaction_time_in_seconds}\n'

        return record_str

    def get_headers(self) -> str:
        return 'id,amount,bank_name,ind_state,hour,minutes,status,transaction_time_in_seconds'