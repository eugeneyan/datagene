# Read about factories at https://github.com/thoughtbot/factory_girl

FactoryGirl.define do
  factory :skill do
    name "MyString"
    description "MyText"
    active true
  end
end
