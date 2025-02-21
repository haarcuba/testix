require 'yaml'
require 'logger'

$log = Logger.new STDERR



desc "run example tests"
task :examples do
    sh "python -m pip install -r examples/requirements.txt"
    sh "python -m pytest -sv examples/tests/test_*.py"
end

desc "run unit tests"
task :units do
    sh "python -m pytest -rA --cov=testix/ --cov-report=term-missing --cov-report=html  -sv test/"
end

desc "make sure we did not forget to include any tests"
task :all_tests_included do
  $log.info "Verifying that we did not forget any dependencies for the All-OK job"
  tests = YAML.load_file '.github/workflows/tests.yaml'
  check_names = tests["jobs"].keys.filter {|job| job != 'All-OK'}
  all_ok = tests['jobs']['All-OK']
  dependencies = all_ok['needs'].to_set
  missing_jobs = check_names.to_set - dependencies
  fail("FAILURE: All-OK missing some tests: #{missing_jobs.to_a}") if missing_jobs.size > 0
  $log.info "no forgotten dependencies, all jobs are included"

  step_names = all_ok['steps'].map {|step| step["name"]}
  missing_jobs = dependencies.to_set - step_names.to_set
  fail("FAILURE: All-OK step-by-step verification missing some tests: #{missing_jobs.to_a}") if missing_jobs.size > 0
  $log.info "verified: a step exists for each of the dependencies"

  all_ok['steps'].each do |step|
    name = step['name']
    next if ! dependencies.include?(name)
    command = step['run']
    referenced = command.include?(name)
    fail("FAILURE: step command for #{name} does not reference '#{name}'") if !referenced
  end
  $log.info "verified: each step references its own dependency"
end

task :enforce_success, [:status] do |t, args|
  status = args[:status]
  fail("FAILURE: received '#{status}' only 'success' is acceptable!") if status != 'success'
end

namespace :documentation do
  desc "install tools needed for documentaion"
  task :setup do
    sh "pip install -r docs/requirements.txt"
  end

  desc "build html documentaion"
  task :html do
    rm_rf "docs/_build"
    sh "sphinx-build -b html  docs/ docs/_build"
  end

  desc "view the docs you just built with firefox"
  task :show do
    sh "firefox docs/_build/index.html"
  end


  namespace :tests do
    desc "run the line_monitor tests"
    task :line_monitor do
      documentation_environment_loaded = ENV['TESTIX_DOCUMENTATION_ENVIRONMENT'] == "True"
      fail('you should source the docs/docs_environment.env script') if ! documentation_environment_loaded
      sh "python -m pytest docs/line_monitor/tests/e2e"
    end
  end
end
