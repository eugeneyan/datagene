class ApplicationController < ActionController::Base
  # Prevent CSRF attacks by raising an exception.
  # For APIs, you may want to use :null_session instead.
  before_filter :configure_permitted_parameters, if: :devise_controller?
  protect_from_forgery with: :exception
  
  
  protected

  def configure_permitted_parameters
    devise_parameter_sanitizer.for(:sign_up) { |u|
    	u.permit( :email, :password, :password_confirmation,
                :first_name, :last_name, :birthday_day, 
                :birthday_month, :birthday_year, :gender, 
                :education, :job_role, :function, :industry, 
                :role )
    }
  end
end

