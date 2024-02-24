PROGRAM MAIN
  USE ALIB
  IMPLICIT NONE

  integer :: num_args, ix
  character(len=128), dimension(:), allocatable :: args ! dynamic list of N 128-length strings.

  integer m

  num_args = command_argument_count()
  allocate(args(num_args))

  if (num_args.gt.1) then
    ix = 1
    call get_command_argument(ix,args(ix))
    WRITE (*,*) args(ix)
  end if


  M = FOO(3)
  WRITE (*,*) M

END PROGRAM MAIN
