from agents.models.interface import ModelTracing

model_01=ModelTracing.ENABLED
print(model_01.include_data())
print(model_01.is_disabled())


model_02=ModelTracing.DISABLED
print(model_02.include_data())
print(model_02.is_disabled())


model_03=ModelTracing.ENABLED_WITHOUT_DATA
print(model_03.include_data())
print(model_03.is_disabled())

