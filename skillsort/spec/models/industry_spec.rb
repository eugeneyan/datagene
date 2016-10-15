require 'spec_helper'

describe Industry do
  # This test checks if the database is populated
  # 30 is an arbitrary chosen value to check data is populated
  it 'should have more than or equal to 30 active industries in the database' do
    Industry.active.count.should be >= 30
  end


  it 'should have a name' do
    industries = Industry.all

    industries.each do |industry|
      industry.name.should_not be_nil
      industry.name.should_not == ''
    end
  end
end
