require 'spec_helper'

describe Function do
  # This test checks if the database is populated
  # 80 is an arbitrary chosen value to check data is populated
  it 'should have more than or equal to 80 active functions in the database' do
    Function.active.count.should be >= 80
  end


  it 'should have a name' do
    functions = Function.all

    functions.each do |function|
      function.name.should_not be_nil
      function.name.should_not == ''
    end
  end
end
