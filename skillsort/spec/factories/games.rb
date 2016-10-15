# Read about factories at https://github.com/thoughtbot/factory_girl

FactoryGirl.define do
  factory :game do
    result "1,5;2,5;3,3;4,2;"
    game_type 1
    version 'v0.2'
    association :user
  end
end
